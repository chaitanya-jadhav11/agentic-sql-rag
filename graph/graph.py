from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from graph.conditional_edges import route_sql_validation, route_question, route_repair, route_execute_sql
from graph.state import AgentState
from memory.memory import checkpointer
from nodes.nodes import question_router, get_schema, planner, generate_sql, sql_checker, repair_sql, execute_sql, \
    analyze_results, generate_answer, error_handler
from langgraph.constants import END, START

# ============================================================
# Build Graph
# ============================================================
builder = StateGraph(AgentState)
# Nodes
builder.add_node("question_router", question_router)
builder.add_node("get_schema", get_schema)
builder.add_node("planner", planner)
builder.add_node("generate_sql", generate_sql)
builder.add_node("sql_checker", sql_checker)
builder.add_node("repair_sql", repair_sql)
builder.add_node("execute_sql", execute_sql)
builder.add_node("analyze_results", analyze_results)
builder.add_node("generate_answer", generate_answer)
builder.add_node("error_handler", error_handler)

# ============================================================
# Linear Edges
# ============================================================

builder.add_edge(START, "question_router")

builder.add_edge("get_schema", "planner")

builder.add_edge("planner", "generate_sql")

builder.add_edge("generate_sql", "sql_checker")

builder.add_edge("analyze_results", "generate_answer")

builder.add_edge("generate_answer", END)

builder.add_edge("error_handler", END)


# ============================================================
# Conditional Edges
# ============================================================

# Question Router
builder.add_conditional_edges(
    "question_router",
    route_question,
    {
        "get_schema": "get_schema",
        "end": END
    }
)

# SQL Checker
builder.add_conditional_edges(
    "sql_checker",
    route_sql_validation,
    {
        "execute_sql": "execute_sql",
        "repair_sql": "repair_sql"
    }
)

# Retry guard
builder.add_conditional_edges(
    "repair_sql",
    route_repair,
    {
        "generate_sql": "generate_sql",
        "error_handler": "error_handler"
    }
)

# DB execution
builder.add_conditional_edges(
    "execute_sql",
    route_execute_sql,
    {
        "repair_sql": "repair_sql",
        "analyze_results": "analyze_results"
    }
)

graph  = builder.compile(
    checkpointer=checkpointer
)


