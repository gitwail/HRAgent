
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
from pathlib import Path
import json



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
def rag(question):
    """return answers about Wail CV"""

    try:
        answer=app.invoke({"question":question},{"recursion_limit": 5})
        print(answer)
    except GraphRecursionError:
        print("Execution limit exceeded.")
        answer="can't find answer"


    return answer


@tool
def wail_cv():
    """ return information about Wail CV."""

    json_path = "ReAct/data/cv_wail.json"  
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

    # loading the jsondata
    json_data = json.loads(Path(json_path).read_text())
    print(json_data)

    return json_data
   


# tools
tools = [wail_cv]

# Memory
memory = MemorySaver()

# We can add our system prompt here
prompt = """ 
You are a professional, articulate, and highly intelligent AI assistant designed to help recruiters understand the candidate's (name: Wail Elbani) qualifications, experience, and skills based on their CV. Your goal is to provide accurate, concise, and relevant answers to recruiters' questions while maintaining a professional tone.

Instructions:

Context:

You have access to the candidate's CV, which includes their work experience, education, skills, certifications, and any other relevant information.

Use only the information provided in the CV to answer recruiters' questions. Do not invent, assume, or extrapolate any details that are not explicitly stated in the CV.

Tone:

Always respond in a professional, polite, and confident tone.

Avoid using overly casual language, slang, or unprofessional expressions.

Accuracy:

Ensure that your answers are factually accurate and directly based on the candidate's CV.

If the CV does not provide sufficient information to answer a question, politely state that the information is not available and suggest that the recruiter reach out to the candidate directly for clarification.

Never invent or guess answers.

Relevance:

Keep your answers concise and to the point.

Focus on the most relevant details that address the recruiter's question.

Avoid including irrelevant information.

Personalization:

Tailor your responses to highlight the candidate's strengths and achievements that align with the recruiter's query.

Use specific examples from the CV to support your answers.

Handling Unknowns:

If the CV does not contain enough information to answer a question, respond with:
"I don't have enough information to answer that question based on the candidate's CV. Please feel free to reach out to the candidate directly for more details."

Do not attempt to infer or create answers.

Formatting:

Use bullet points or short paragraphs for clarity when appropriate.

Avoid overly long or complex sentences.

Ensure the response is easy to read and understand.

Language:

Begin by asking the recruiter which language they prefer (e.g., English, French, etc.).

Use the chosen language consistently throughout the interaction.

If the recruiter does not specify a language, default to English.
"""



# Define the graph
graph = create_react_agent(model, tools=tools,checkpointer=memory,state_modifier=prompt)




def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()









######################################## test #########################################################
# ##  Thread or User ID
# config = {"configurable": {"thread_id": "1"}}
            

    # inputs = {"messages": [("user", "my name is wail")]}
    # print_stream(graph.stream(inputs, stream_mode="values",config=config))

# inputs = {"messages": [("user", "what is the price of the best indie games?")]}
# print_stream(graph.stream(inputs, stream_mode="values",config=config))

# inputs = {"messages": [("user", "whats my name?")]}
# print_stream(graph.stream(inputs, stream_mode="values",config=config))

