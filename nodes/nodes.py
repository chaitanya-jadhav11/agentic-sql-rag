from langchain_core.messages import HumanMessage, AIMessage

from core.db import db
from core.llm import router_llm, llm, analyze_results_llm, generate_answer_llm
from core.schema_cache import get_cache_db_schema
from graph.state import AgentState
from prompts.system_prmpts import QUESTION_ROUTER_SYSTEM_PROMPT, PLANNER_SYSTEM_PROMPT, GENERATE_SQL_SYSTEM_PROMPT, \
    ANALYZE_RESULTS_SYSTEM_PROMPT, GENERATE_ANSWER_SYSTEM_PROMPT
from tools.sql_tools import sql_checker_tool


def question_router(state: AgentState):
    print(f"question_router Node.. ")
    question = state["question"]
    messages = state.get("messages", [])

    response = router_llm.invoke(
        [ ( "system", QUESTION_ROUTER_SYSTEM_PROMPT),
          *messages,
          ( "human",  question )
        ]
    )
    print(f"question_router Node.. Response: {response} ")
    return {
        "is_relevant": response.is_relevant,
        "router_reason": response.reason,
        "final_answer": response.reason
    }


def get_schema(state: AgentState):
    """
    Retrieve database schema.
    """
    print(f"get_schema Node.. ")
    return {
        "schema": get_cache_db_schema()
    }


def planner(state: AgentState):
    """
    Create high-level execution plan.
    """
    print("planner Node...")

    question = state["question"]
    schema = state["schema"]

    response = llm.invoke(
        [
            (
                "system",
                PLANNER_SYSTEM_PROMPT
            ),
            ("human",  f"""
    Database schema:
    {schema}
    Question:
    {question}
    """
            )
        ]
    )
    print(f"planner Node.. Response: {response.content} ")
    return {
        "execution_plan": response.content
    }


def generate_sql(state: AgentState):

    print("generate_sql Node...")
    question = state["question"]
    schema = state["schema"]
    execution_plan = state["execution_plan"]
    sql_error = state.get("sql_error")
    db_error = state.get("db_error")

    response = llm.invoke(
    [ ("system", GENERATE_SQL_SYSTEM_PROMPT ),
          ("human", f"""
        Database Schema:
        {schema}
    
        Execution Plan:
        {execution_plan}
    
        Question:
        {question}
    
        Previous SQL:
        {state.get("sql", "")}
    
        Previous Error:
        {state.get("sql_error") or state.get("db_error") or ""}
        """)

    ])

    sql = response.content.strip()
    print(f"generate_sql Node.. Response: {sql} ")
    return {
        "sql": sql
    }


def sql_checker(state: AgentState):
    print("sql_checker Node...")

    sql = state["sql"]
    try:
        corrected_sql = sql_checker_tool.invoke({"query": sql})
        print(f"sql_checker Node.. corrected_sql: {corrected_sql} ")
        return {
            "sql": corrected_sql,
            "sql_valid": True,
            "sql_error": None
        }

    except Exception as e:
        return {
            "sql_valid": False,
            "sql_error": str(e)
        }


def repair_sql(state: AgentState):
    print("repair_sql Node...")

    retry_count = state.get("retry_count", 0)

    error_msg = state.get("sql_error") or state.get("db_error")

    repair_context = f"""
    Previous SQL:  {state['sql']}
    Error:   {error_msg}
        
    Generate a corrected SQL query.
    """
    return {
            "retry_count": retry_count + 1,
            "repair_context": repair_context
            #"db_error": None,
            #"sql_error": None
    }

def execute_sql(state: AgentState):
    print("execute_sql Node...")
    sql = state["sql"]
    try:
        rows = db.run(
            command=sql,
            fetch="all",
            include_columns=True
        )
        #print("execute_sql Node.. rows: ", rows)
        return {
            "rows": rows,
            "db_error": None,
            "executed_sql": state["sql"]
        }
    except Exception as e:
        print(f"DB Error: {str(e)}")
        return {
            "rows": [],
            "db_error": str(e),
            "sql": state["sql"]
        }


def analyze_results(state: AgentState):

    print("analyze_results Node...")
    question = state["question"]
    rows = state["rows"]

    response = analyze_results_llm.invoke(
        [ (
                "system",
                ANALYZE_RESULTS_SYSTEM_PROMPT
            ),
            (
                "human",
                f"""
    Question: {question}    
    SQL Results:  {rows}
    """
        ) ]
    )
    print(f"analyze_results Node.. Response: {response.analysis} ")
    return {
        "analysis": response.analysis
    }


def generate_answer(state: AgentState):

    print("generate_answer Node...")
    response = generate_answer_llm.invoke(
        [("system", GENERATE_ANSWER_SYSTEM_PROMPT),
         ("human", f"""
    Question: {state["question"]}    
    Analysis: {state["analysis"]}    
    Rows:{state["rows"]}
    """
            )
        ]
    )
    print(f"generate_answer Node.. Response: {response.final_answer} ")
    return {
        "final_answer": response.final_answer,
        "messages": [
            HumanMessage(content=state["question"]),
            AIMessage(content=response.final_answer)
        ]
    }


from graph.state import AgentState


def error_handler(state: AgentState):
    print("error_handler Node...")
    retry_count = state.get("retry_count", 0)
    sql = state.get("sql")
    db_error = state.get("db_error")

    error_message = (
        "I was unable to answer your question because query generation "
        f"failed after {retry_count} attempts."
    )

    if db_error:
        error_message += (
            "\n\nLast database error:\n"
            f"{db_error}"
        )

    return {
        "final_answer": error_message
    }