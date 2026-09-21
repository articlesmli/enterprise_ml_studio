from fastmcp import FastMCP
import psycopg2
import os

mcp = FastMCP("Enterprise ML Studio MCP Server")

@mcp.tool()
def get_recent_ml_metrics() -> str:
    """Fetch the latest model training runs and status from the database."""
    conn = psycopg2.connect(os.getenv("DATABASE_URL", "postgresql://ml_user:ml_password@ml-postgres:5432/ml_studio_db"))
    cursor = conn.cursor()
    cursor.execute("SELECT model_name, metrics, created_at FROM model_registry ORDER BY created_at DESC LIMIT 5;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return str(rows)

if __name__ == "__main__":
    mcp.run()
