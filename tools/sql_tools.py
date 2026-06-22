
from langchain_community.tools.sql_database.tool import QuerySQLCheckerTool
from core.db import db
from core.llm import llm

sql_checker_tool = QuerySQLCheckerTool(
    db=db,
    llm=llm
)