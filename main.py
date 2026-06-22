from pathlib import Path
from dotenv import load_dotenv

from graph.graph import graph


load_dotenv(override=True)
#config = {"configurable": {"thread_id": "4"}}

from fastapi import FastAPI
from api.chat_api import router

app = FastAPI()

app.include_router(router)


def main():
    graph.get_graph(xray=1).draw_mermaid_png(
        output_file_path="workflow_image/app_graph.png")

    #snapshot = app.get_state(config)

    #print("\n===== Snapshot =====")
    #print(snapshot.values)

   # res = app.invoke(
   #     {
   #         "question": "Who spent the least among them??",
   #         "retry_count": 0
   #     },
    #    config=config
    #)
    #print(f" final_answer:- { res["final_answer"]} ")
    #print(f" retry_count:- { res["retry_count"]}")
    #print(f" messages:- { res["messages"]}")

# uv run -m app.main
if __name__ == "__main__":
    main()
