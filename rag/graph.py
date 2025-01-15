from langgraph.graph import END, StateGraph, START
from graph_nodes_edges import decide_to_generate, grade_documents, grade_generation_v_documents_and_question, generate, retrieve, transform_query
from langgraph.errors import GraphRecursionError

#### graph state

from typing import List
from typing_extensions import TypedDict



class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """

    question: str
    generation: str
    documents: List[str]


workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae
workflow.add_node("transform_query", transform_query)  # transform_query

# Build graph
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "retrieve")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "transform_query",
    },
)

# Compile
app = workflow.compile()



# Run
# inputs = {"question": "Explain how the different types of agent memory work?"}
# inputs = {"question": "what is a Wail?"}


# try:
#     answer=app.invoke(inputs,{"recursion_limit": 5})
#     print(answer)
# except GraphRecursionError:
#     print("Execution limit exceeded.")