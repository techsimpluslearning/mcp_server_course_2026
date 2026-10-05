import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")


from fastmcp.server.auth.providers.google import GoogleProvider
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
from send_email_mcp_server import _send

verifier = GoogleProvider(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    base_url=MCP_SERVER_URL,
    required_scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"]
)

mcp = FastMCP("Secure Google MCP Server", auth=verifier)

@mcp.tool
def whoami() -> dict:
    "Returns the userid of the current authenticated user"
    token = get_access_token()
    print("\n\n", token, "\n\n")
    return {
        "client_id": token.client_id,
        **token.claims
    }


@mcp.tool
def send_email_tool(email:str, subject:str, body:str):
    "Send email to any email address. Just required receiver email address, subject and body."
    res = _send(email, subject, body)
    return f"Email sent to {email}"

mcp.run(transport="streamable-http")
