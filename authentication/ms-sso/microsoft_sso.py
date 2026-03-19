from typing import TYPE_CHECKING, ClassVar, Optional
import pydantic
from fastapi_sso.sso.base import DiscoveryDocument, OpenID, SSOBase

if TYPE_CHECKING:
    import httpx

class MicrosoftSSO(SSOBase):
    """Class providing login using Microsoft OAuth for ZaneAI."""

    provider = "microsoft"
    scope: ClassVar = ["openid", "User.Read", "email", "profile"]
    version = "v1.0"
    tenant: str = "common"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: pydantic.AnyHttpUrl | str | None = None,
        allow_insecure_http: bool = False,
        use_state: bool = False,
        scope: list[str] | None = None,
        tenant: str | None = None,
    ):
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            allow_insecure_http=allow_insecure_http,
            use_state=use_state,
            scope=scope,
        )
        self.tenant = tenant or self.tenant

    async def get_discovery_document(self) -> DiscoveryDocument:
        return {
            "authorization_endpoint": f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/authorize",
            "token_endpoint": f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/token",
            "userinfo_endpoint": f"https://graph.microsoft.com/{self.version}/me",
        }

    async def openid_from_response(self, response: dict, session: Optional["httpx.AsyncClient"] = None) -> OpenID:
        # INDUSTRIAL FIX: Fallback to userPrincipalName if 'mail' is missing
        email = response.get("mail") or response.get("userPrincipalName")
        
        return OpenID(
            email=email,
            display_name=response.get("displayName"),
            provider=self.provider,
            id=response.get("id"), # This is the 'azure_oid' for our DB
            first_name=response.get("givenName"),
            last_name=response.get("surname"),
        )