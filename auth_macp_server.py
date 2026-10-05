JWT_SECRET_KEY = "98c36e1e-9ff0-4ec6-9fd5-42c1f816f817"
JWT_ALGO = "HS256"
JWT_ISSUER = "http://localhost:8001"
JWT_EXPIRE_HOURS = 1
JWT_AUDIENCE = "my-mcp-server"



from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.dependencies import get_access_token

verifier = JWTVerifier(
    public_key=JWT_SECRET_KEY,
    algorithm=JWT_ALGO,
    issuer=JWT_ISSUER,
    audience=JWT_AUDIENCE
)


mcp = FastMCP("Secure MCP Server", auth=verifier)

@mcp.tool
def whoami() -> dict:
    "Returns the userid of the current authenticated user"
    token = get_access_token()
    print("\n\n", token, "\n\n")
    return {
        "client_id": token.client_id,
        "email": token.claims.get("email", "")
    }


mcp.run(transport="streamable-http")


