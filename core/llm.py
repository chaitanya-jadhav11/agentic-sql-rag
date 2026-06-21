from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from graph.state import QuestionRouterOutput, AnalysisOutput, FinalAnswerOutput

load_dotenv(override=True)

llm = ChatOpenAI(
    model="gpt-5",
    temperature=0
)

router_llm = llm.with_structured_output(
    QuestionRouterOutput
)

analyze_results_llm = ChatOpenAI(
    model="gpt-5",
    temperature=0
).with_structured_output(AnalysisOutput)

generate_answer_llm = ChatOpenAI(
    model="gpt-5",
    temperature=0
).with_structured_output(FinalAnswerOutput)
