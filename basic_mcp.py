from fastmcp import FastMCP

mcp = FastMCP(
    name="Simple MCP Server"
)


@mcp.tool
def add(a:int, b:int) -> int:
    "Accept two numbers and return sum of those numbers"
    return a + b


##### transport => stdio, http 
mcp.run(transport="streamable-http")
        

