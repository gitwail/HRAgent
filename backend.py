from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple

# Import your chatbot logic
from ReAct.prebuilt_react_agent import graph

# Initialize FastAPI app
app = FastAPI()

class ChatRequest(BaseModel):
    history: List[Tuple[str, str]]
    msg: str
    thread_id: str = "1"  # Default thread ID


class ChatResponse(BaseModel):
    content: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Prepare the inputs for the graph with correct message format
        inputs = {"messages": [("user", request.msg)]}

        
        config = {"configurable": {"thread_id": request.thread_id}}

        # Stream response from the graph
        stream = graph.stream(inputs, stream_mode="values", config=config)

        # Get chatbot response
        chatbot_reply = ""
        for s in stream:
            message = s["messages"][-1]
            chatbot_reply = message[1] if isinstance(message, tuple) else message.content

        return {"content": chatbot_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
