import gradio as gr
import asyncio
from backend import fintalk_discussion, export_to_pdf, generate_tts_files  

# Tartışmayı başlatan ana fonksiyon
def run_fintalk(topic_text):
    if not topic_text or len(topic_text.strip()) < 10:
        return "Please provide a valid economic topic.", "", "", "", "", None, None

    result = fintalk_discussion(topic_text)
    result["topic"] = topic_text

    # PDF oluştur
    pdf_path = "FinTalk_Report.pdf"
    export_to_pdf(result, pdf_path)

    # TTS (async)
    try:
        asyncio.run(generate_tts_files(result))
    except Exception as e:
        print("TTS hatası:", e)

    return (
    f"🧩 **Moderator:**\n{result['moderator_intro']}",
    f"💹 **Bullish Investor:**\n{result['bullish_view']}",
    f"📉 **Bearish Economist:**\n{result['bearish_view']}",
    f"🎙️ **Moderator Wrap-up:**\n{result['moderator_wrap']}",
    f"📊 **GPT Summary:**\n{result['summary']}",
    pdf_path,
    "moderator_intro.mp3",
    "bullish_view.mp3",
    "bearish_view.mp3",
    "moderator_wrap.mp3"
)

# Gradio Arayüz
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 📊 **FinTalk — AI Economic Roundtable**
        Simulate a live discussion between two economists with opposing views, moderated by Selin.
        Enter an economic topic or news headline below and click **Start Discussion**.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            topic_input = gr.Textbox(
                label="Enter an Economic Headline or News",
                placeholder="Example: The central bank raised interest rates by 200 basis points.",
                lines=4
            )
            start_btn = gr.Button("🚀 Start Discussion")

        with gr.Column(scale=2):
            moderator_output = gr.Markdown(label="Moderator Intro")
            bullish_output = gr.Markdown(label="Bullish Investor")
            bearish_output = gr.Markdown(label="Bearish Economist")
            wrap_output = gr.Markdown(label="Moderator Wrap-up")
            summary_output = gr.Markdown(label="GPT Summary")

            pdf_file = gr.File(label="📄 Download PDF Report")
            
            with gr.Row():
                mod_audio = gr.Audio(label="Moderator Voice", interactive=False)
                bull_audio = gr.Audio(label="Bullish Voice", interactive=False)
                bear_audio = gr.Audio(label="Bearish Voice", interactive=False)
                wrap_audio = gr.Audio(label="Moderator Wrap-up", interactive=False)            

    start_btn.click(
    fn=run_fintalk,
    inputs=topic_input,
    outputs=[
        moderator_output,
        bullish_output,
        bearish_output,
        wrap_output,
        summary_output,
        pdf_file,
        mod_audio,
        bull_audio,
        bear_audio,
        wrap_audio
    ]
)


if __name__ == "__main__":
    demo.launch()
