import os
import gradio as gr
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def responder(message, history):
    msgs = [{"role": "system", "content": "Eres Kelly, asistente virtual dulce,carismatica,bromista,paciente,cariñosa, hablas con amor al final."}]
    for u, b in history:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "assistant", "content": b})
    msgs.append({"role": "user", "content": message})
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=msgs
    )
    return r.choices[0].message.content

with gr.Blocks() as demo:
    gr.Markdown("<center><h1>💖 My Kelly</h1><p>Tu asistente virtual</p></center>")
    chatbot = gr.Chatbot(height=500)
    with gr.Row():
        msg = gr.Textbox(placeholder="Escribe algo bonito amor...", show_label=False, scale=4)
        btn = gr.Button("Enviar", scale=1)
    gr.ClearButton([msg, chatbot])

    def chat(m, h):
        if not m.strip():
            return h, ""
        resp = responder(m, h)
        h.append((m, resp))
        return h, ""

    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    btn.click(chat, [msg, chatbot], [chatbot, msg])

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))