import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from microsoft_sso import MicrosoftSSO

load_dotenv()

app = FastAPI(title="ZaneAI SSO Demo")

# INDUSTRIAL PRACTICE: Use a secret key to sign session cookies
app.add_middleware(SessionMiddleware, secret_key="ZANE_AI_DEMO_SECRET_KEY")

sso = MicrosoftSSO(
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET"),
    tenant=os.getenv("AZURE_TENANT_ID"),
    redirect_uri=os.getenv("REDIRECT_URI"),
    allow_insecure_http=True
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = request.session.get("user")
    
    # If user is logged in, show their profile and a logout button
    if user:
        return f"""
        <html>
            <body style="font-family: sans-serif; text-align: center; padding-top: 100px;">
                <h1>Welcome to ZaneAI, {user['display_name']}!</h1>
                <p>Logged in as: <strong>{user['email']}</strong></p>
                <div style="margin-top: 20px;">
                    <a href="/auth/logout" style="color: red; font-weight: bold;">Logout of ZaneAI</a>
                </div>
            </body>
        </html>
        """
    
    # Otherwise, show the login button
    return """
    <html>
        <body style="font-family: sans-serif; text-align: center; padding-top: 100px;">
            <h1>ZaneAI Portal</h1>
            <a href="/auth/microsoft" style="background-color: #00a4ef; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                Log in with Microsoft SSO
            </a>
        </body>
    </html>
    """

@app.get("/auth/microsoft")
async def microsoft_login():
    with sso:
        return await sso.get_login_redirect()

@app.get("/auth/callback")
async def microsoft_callback(request: Request):
    with sso:
        user_data = await sso.verify_and_process(request)
    
    # INDUSTRIAL PRACTICE: Store user info in a session cookie
    request.session["user"] = {
        "id": user_data.id,
        "email": user_data.email,
        "display_name": user_data.display_name
    }
    
    # Redirect back to home instead of showing raw JSON
    return RedirectResponse(url="/")

@app.get("/auth/logout")
async def logout(request: Request):
    # 1. Clear local ZaneAI session
    request.session.clear()
    
    # 2. INDUSTRIAL CHOICE: Do we log out of Microsoft too?
    # If you want to force Microsoft sign-out, redirect to this URL:
    tenant = os.getenv("AZURE_TENANT_ID") or "common"
    post_logout_url = "http://localhost:8000" # Where MS sends user AFTER MS logout
    
    ms_logout_url = (
        f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={post_logout_url}"
    )
    
    return RedirectResponse(url=ms_logout_url)