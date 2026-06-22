from typing import TypedDict, Optional, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class AgentState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]

    question: str
    is_relevant: bool
    schema: Optional[str]
    execution_plan: Optional[str]
    sql: Optional[str]
    sql_valid: bool
    db_error: Optional[str]
    sql_error: Optional[str]
    executed_sql : Optional[str]
    rows: list
    analysis: Optional[str]
    final_answer: Optional[str]
    repair_context: Optional[str]
    retry_count: int


class QuestionRouterOutput(BaseModel):
    is_relevant: bool = Field(
        description="Whether the question can be answered using the ecommerce database."
    )

    reason: str = Field(
        description="Short explanation for the decision."
    )

from pydantic import BaseModel, Field


class AnalysisOutput(BaseModel):
    analysis: str = Field(
        description="Summary and insights derived from SQL results."
    )

class FinalAnswerOutput(BaseModel):
    final_answer: str = Field(
        description="User-facing answer."
    )