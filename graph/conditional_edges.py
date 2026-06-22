# ============================================================
# Conditional Edge Functions
# ============================================================
from graph.state import AgentState


def route_question(state: AgentState):
    print(f"In route_question...")

    if state["is_relevant"]:
        return "get_schema"

    return "end"


def route_sql_validation(state: AgentState):
    print(f"In route_sql_validation...")
    if state["sql_valid"]:
        return "execute_sql"

    return "repair_sql"


def route_repair(state: AgentState):
    print(f"In route_repair...")
    if state["retry_count"] >= 3:
        print("retry_count >= 3. redirecting to error_handler ")
        return "error_handler"

    return "generate_sql"


def route_execute_sql(state: AgentState):
    print(f"In route_execute_sql...")

    if state["db_error"]:
        return "repair_sql"

    return "analyze_results"
