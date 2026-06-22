
from graph.graph import app

def test_happy_path():
    result = app.invoke(
        {
            "question": "How many customers are there?",
            "retry_count": 0
        }
    )
    print(result["final_answer"])
    assert result["final_answer"] is not None

d