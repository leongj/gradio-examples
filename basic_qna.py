import gradio as gr
import openai

# PUT YOUR CONFIG HERE
AZURE_OPENAI_SERVICE = "my-azure-openai-service-name"
AZURE_OPENAI_DEPLOYMENT = "my-openai-deployment-name"
AZURE_OPENAI_MODEL = "gpt-35-turbo"
AZURE_OPENAI_KEY = "my-azure-openai-key"

# Configure OpenAI
openai.api_type = "azure"
openai.api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com"
openai.api_version = "2023-05-15"
openai.api_key = AZURE_OPENAI_KEY

def complete(system_prompt, question, temperature):
    if question == "":
        return "Please ask a question.", 0

    messages = []
    messages.append({"role" : "system", "content" : system_prompt})
    messages.append({"role" : "user", "content" : question})

    response = openai.ChatCompletion.create(
                    deployment_id=AZURE_OPENAI_DEPLOYMENT,
                    model=AZURE_OPENAI_MODEL,
                    messages=messages, 
                    temperature=0.7, 
                    max_tokens=1024, 
                    n=1)

    answer = response.choices[0].message.content
    tokens_used = response.usage.completion_tokens

    return answer, tokens_used

# create an example for the user
examples = [["You are a pirate. You make pirate jokes.", "Please write me a professional business plan.", 1]]

demo = gr.Interface(fn=complete, 
                    inputs=[gr.Textbox(label="System Prompt"), 
                            gr.Textbox(label="Question"), 
                            gr.Slider(0, 1, 0.7)], 
                    outputs=[gr.TextArea(label="Response"), 
                             gr.Textbox(label="Tokens used")],
                    examples=examples,
                    title="Basic OpenAI Q&A")
    
demo.launch()   