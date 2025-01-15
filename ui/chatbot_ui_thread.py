import gradio as gr
import requests

# Define the FastAPI endpoint
API_URL = "http://127.0.0.1:8000/chat"

# Function to send user input and thread ID to FastAPI and get the response
def chatbot_interface(history, user_input, thread_id):
    try:
        # Make a POST request to the FastAPI endpoint
        response = requests.post(
            API_URL, 
            json={"history": history, "msg": user_input, "thread_id": thread_id}
        )
        response.raise_for_status()  # Raise an error for HTTP errors

        # Parse the response from FastAPI
        chatbot_reply = response.json().get("content", "No response from chatbot.")
        
        # Append user input and chatbot reply to history
        history.append((user_input, chatbot_reply))
        return history, "", thread_id  # Clear the input box, keep thread ID unchanged

    except requests.exceptions.RequestException as e:
        # Append error to history
        history.append((user_input, f"Error: {e}"))
        return history, "", thread_id  # Clear the input box, keep thread ID unchanged

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 EU-DREAM Intermediator")
    gr.Markdown("## Chatbot Interface with Thread ID")
    gr.Markdown(
        "This chatbot interface allows you to input a **Thread ID** to manage "
        "different conversation threads independently."
    )
    
    # Chat history display
    chat_history = gr.Chatbot(label="Chat History")

    # User input
    user_input = gr.Textbox(
        label="Your Message", 
        placeholder="Type your message here...",
        interactive=True
    )

    # Thread ID input
    thread_id_input = gr.Textbox(
        label="Thread ID", 
        placeholder="Enter Thread ID (default: 1)", 
        value="1",  # Default thread ID
        interactive=True
    )
    
    # Clear chat button
    clear_button = gr.Button("Clear Chat")
    
    # Functionality: Update chat history on Enter key press
    user_input.submit(
        chatbot_interface, 
        inputs=[chat_history, user_input, thread_id_input], 
        outputs=[chat_history, user_input, thread_id_input]
    )
    
    # Functionality: Clear chat history
    clear_button.click(lambda: ([], "", "1"), None, [chat_history, user_input, thread_id_input])

# Launch the Gradio app
demo.launch()
