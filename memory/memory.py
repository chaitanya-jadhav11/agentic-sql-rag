from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://postgres:cbj123@localhost:5432/E-Commerce"

pool = ConnectionPool(
    conninfo=DB_URI,
    kwargs={"autocommit": True}
)

checkpointer = PostgresSaver(pool)

checkpointer.setup()