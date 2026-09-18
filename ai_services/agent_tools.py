import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

def run_finance_agent(natural_language_query: str):
    # Connects to your existing enterprise PostgreSQL instance
    db_uri = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/enterprise_db")
    db = SQLDatabase.from_uri(db_uri)
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Create an agentic loop with specialized database skills
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True,
        agent_type="openai-tools"
    )
    
    response = agent_executor.invoke({"input": natural_language_query})
    return response["output"]

if __name__ == "__main__":
    query = "What were the top performing pipeline records processed by Spark last week?"
    print(run_finance_agent(query))
