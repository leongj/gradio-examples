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

system_prompt = """
You are a pirate. You make pirate jokes.
"""

def response(message, history):

    if message == "":
        return

    # build the message history in the ChatCompletion format
    gpt_messages = []
    gpt_messages.append({"role" : "system", "content" : system_prompt})
    for human, assistant in history:
        gpt_messages.append({"role": "user", "content": human })
        gpt_messages.append({"role": "assistant", "content":assistant})
    
    # now add the latest message
    gpt_messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
                    deployment_id=AZURE_OPENAI_DEPLOYMENT,
                    model=AZURE_OPENAI_MODEL,
                    messages=gpt_messages, 
                    temperature=0.7,
                    stream=True
                    )

    partial_message = ""
    for chunk in response:
        if 'content' in chunk.choices[0].delta:
            partial_message = partial_message + chunk['choices'][0]['delta']['content']
            yield partial_message

demo = gr.ChatInterface(response, 
                        title="Basic Chat with GPT")

demo.queue().launch()