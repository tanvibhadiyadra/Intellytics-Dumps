# MS Azure SSO – ZaneAI Demo

A minimal Python demo of **Microsoft Azure Single Sign-On** using FastAPI and OpenID Connect (OAuth 2.0 Authorization Code Flow).

---

### 1. Clone & Install
```bash
git clone https://github.com/tanvibhadiyadra/MS_SSO.git
cd MS_SSO
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:
```env
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
REDIRECT_URI=http://localhost:8000/auth/callback
```

### 3. Run
```bash
uvicorn main:app --reload --port 8000
```
Open → [http://localhost:8000](http://localhost:8000)
---

## 🔄 Auth Flow

```
User → /auth/microsoft → Azure AD Login → /auth/callback → Session Created → Dashboard
```

| Route | Description |
|---|---|
| `GET /` | Home — login button or user dashboard |
| `GET /auth/microsoft` | Redirects to Microsoft login |
| `GET /auth/callback` | Handles Azure redirect, creates session |
| `GET /auth/logout` | Clears session + signs out from Microsoft |

---

## 🏗️ Azure Setup (One-Time)

1. **Register App** — Azure Portal → App Registrations → New Registration
   - Redirect URI: `http://localhost:8000/auth/callback`
2. **Fix Token Version** — Manifest → set `accessTokenAcceptedVersion: 2`
3. **Expose API** — Add scope `access_as_user`
4. **Create Secret** — Certificates & Secrets → New Client Secret (180 days)
5. **Copy IDs** — Tenant ID, Client ID, Secret Value → paste into `.env`

---

## 📁 Project Structure

```
MS_SSO/
├── main.py            # FastAPI app & routes
├── microsoft_sso.py   # MicrosoftSSO client config
├── requirements.txt   # Dependencies
└── .env               # Azure credentials (not committed)
```

---

## ⚠️ Notes

- `allow_insecure_http=True` is set for **local dev only** — remove in production
- Never commit `.env` to Git
- Full documentation: see project Word doc

---

## 📄 License

Internal demo — Intellytics Solutions LLP
