import gradio as gr
import requests

# Define the FastAPI endpoint
API_URL = "http://127.0.0.1:8000/chat"

def chatbot_interface(history, user_input, thread_id):
    try:
        response = requests.post(
            API_URL, 
            json={"history": history, "msg": user_input, "thread_id": thread_id}
        )
        response.raise_for_status()
        chatbot_reply = response.json().get("content", "No response from chatbot.")
        history.append((user_input, chatbot_reply))
        return history, "", thread_id
    except requests.exceptions.RequestException as e:
        history.append((user_input, f"Error: {e}"))
        return history, "", thread_id

# Function to handle example message clicks
def send_example(example_text, history, thread_id):
    return chatbot_interface(history, example_text, thread_id)

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Recruiter Chatbot")
    gr.Markdown("## Chatbot Interface with Thread ID")
    
    with gr.Row():
        with gr.Column(scale=2):
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
                value="1",
                interactive=True
            )
            
            # Clear chat button
            clear_button = gr.Button("Clear Chat")
        
        # Example messages column
        with gr.Column(scale=1):
            gr.Markdown("### Example Messages")
            example_messages = [
                "List the projects that Wail have worked on",
              
            ]
            
            # Create buttons for each example message
            for msg in example_messages:
                example_btn = gr.Button(f"💬 {msg}")
                example_btn.click(
                    send_example,
                    inputs=[gr.Textbox(value=msg, visible=False), chat_history, thread_id_input],
                    outputs=[chat_history, user_input, thread_id_input]
                )
    
    # Regular message submission
    user_input.submit(
        chatbot_interface, 
        inputs=[chat_history, user_input, thread_id_input],
        outputs=[chat_history, user_input, thread_id_input]
    )
    
    # Clear chat functionality
    clear_button.click(
        lambda: ([], "", "1"),
        None,
        [chat_history, user_input, thread_id_input]
    )

demo.launch()