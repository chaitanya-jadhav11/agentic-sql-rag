from fastapi import APIRouter

from api.chat_models import ChatResponse, ChatRequest
from graph.graph import graph

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    config = {
        "configurable": {
            "thread_id": request.user_id +"-" + request.conversation_id
        }
    }

    result = graph.invoke(
        {
            "question": request.question,
            "retry_count": 0
        },
        config=config
    )

    return ChatResponse(
        answer=result["final_answer"]
    )