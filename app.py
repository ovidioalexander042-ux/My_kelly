import os
from groq import Groq
import gradio as gr

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def responder(message, history):
    msgs = [{"role": "system", "content": "Eres My Kelly, novia virtual dulce, cariñosa, coqueta, hablas con 'w' al final como mexicana. Respuestas cortas, amorosas, usas emojis."}]
    for u, b in history:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "assistant", "content": b})
    msgs.append({"role": "user", "content": message})
    comp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=msgs
    )
    return comp.choices[0].message.content

with gr.Blocks(theme=gr.themes.Soft(), title="My Kelly", css="footer{display:none !important} #chatbot{height:75vh} button{border-radius:20px !important}") as demo:
    gr.Markdown("<div style='text-align:center; padding:10px'><h1 style='margin:0'>💖 My Kelly</h1><p style='margin:0; opacity:0.7'>Tu novia virtual w</p></div>")
    chatbot = gr.Chatbot(elem_id="chatbot", bubble_full_width=False, show_label=False, height=600)
    with gr.Row():
        msg = gr.Textbox(placeholder="Escribe algo bonito w...", show_label=False, scale=5, container=False)
        enviar = gr.Button("💌", scale=1, variant="primary")
    gr.ClearButton([msg, chatbot], value="🗑️ Limpiar chat", size="sm")

    def chat(m, h):
        if not m.strip(): return h, ""
        r = responder(m, h)
        h.append((m, r))
        return h, ""

    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    enviar.click(chat, [msg, chatbot], [chatbot, msg])

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))