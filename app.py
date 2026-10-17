import os
from groq import Groq
import gradio as gr

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def responder(message, history):
    msgs = [{"role": "system", "content": "Eres MY KELLY, hablas con w al final."}]
    for u, b in history:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "assistant", "content": b})
    msgs.append({"role": "user", "content": message})
    comp = client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs)
    return comp.choices[0].message.content

demo = gr.ChatInterface(fn=responder, title="MY KELLY")
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
