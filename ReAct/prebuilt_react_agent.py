
import os
from dotenv import load_dotenv
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rag')))
from langgraph.errors import GraphRecursionError
from graph import app
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from typing import Literal
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Load environment variables from .env file
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_ENDPOINT"]=os.getenv("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

# First we initialize the model we want to use.
model = ChatOpenAI(model="gpt-4o", temperature=0)



@tool
def game_prices(game_name):
    """give the price of a game"""
    game_name = game_name.strip().lower()  # Normalize the game name to lowercase
    if game_name == "hollow knight".lower():
        return "100"
    if game_name == "metro".lower():
        return "30"
    
    return "game not found"

@tool
def rag(question):
    """return answers about Indie games"""

    try:
        answer=app.invoke({"question":question},{"recursion_limit": 5})
        print(answer)
    except GraphRecursionError:
        print("Execution limit exceeded.")
        answer="can't find answer"


    return answer
   

@tool
def get_bestgame():
    """ return a list of games that I like"""
    return "Hollow knight"


# tools
tools = [game_prices, get_bestgame,rag]

# Memory
memory = MemorySaver()

# We can add our system prompt here
prompt = "You are a helpful assistant and an expert in indie games."

# Define the graph
graph = create_react_agent(model, tools=tools,checkpointer=memory,state_modifier=prompt)




def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

# ##  Thread or User ID
# config = {"configurable": {"thread_id": "1"}}
            

    # inputs = {"messages": [("user", "my name is wail")]}
    # print_stream(graph.stream(inputs, stream_mode="values",config=config))

# inputs = {"messages": [("user", "what is the price of the best indie games?")]}
# print_stream(graph.stream(inputs, stream_mode="values",config=config))

# inputs = {"messages": [("user", "whats my name?")]}
# print_stream(graph.stream(inputs, stream_mode="values",config=config))

