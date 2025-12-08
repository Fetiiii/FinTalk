import os
import re
from typing import Dict
from dotenv import load_dotenv
from llama_cpp import Llama
from openai import OpenAI
import edge_tts
import asyncio
import reportlab

load_dotenv()  

model_path = r"C:/Users/cagri/.lmstudio/models/QuantFactory/Llama-3-8B-Instruct-Finance-RAG-GGUF/Llama-3-8B-Instruct-Finance-RAG.Q4_K_S.gguf"

llm = Llama(
    model_path=model_path,
    n_ctx=4096,
    n_threads=6,   
    n_batch=512,
    verbose=False
)


OPENAI_API_KEY = os.getenv("API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("API_KEY bulunamadı. Lütfen .env veya sistem değişkenlerine ekleyin.")
client = OpenAI(api_key=OPENAI_API_KEY)
SUMMARY_MODEL = os.getenv("SUMMARY_MODEL", "gpt-4o-mini")


SYSTEM_MODERATOR = (
    "You are Selin, the moderator of an economics roundtable. "
    "Be neutral, brief, and structured. Guide the flow without giving opinions."
)

SYSTEM_BULLISH = (
   """You are Bullish Investor, an optimistic economist who focuses on growth, market confidence, and positive catalysts.
    Be analytical and persuasive. Mention at least two concrete macro or market factors that support your optimism 
    (e.g., improved investor sentiment, fiscal stimulus, or sector resilience). 
    Respond in 2–3 detailed paragraphs and conclude with one confident takeaway."""
)

SYSTEM_BEARISH = (
    "You are Bearish Economist, a cautious macroeconomist who highlights downside risks "
    "(inflation persistence, liquidity stress, policy uncertainty). Be analytical; end with one cautionary insight."
)


_META_PATTERNS = [
    r"(?i)\bnote:\b.*",                 
    r"(?i)\bi am (selin|bullish|bearish).*$", 
    r"(?i)\bthis response was written\b.*",
    r"(?i)\bplease review\b.*",
    r"(?i)\bclarity and readability\b.*",
]
def _clean(text: str) -> str:
    cleaned = text.strip()
    for pat in _META_PATTERNS:
        cleaned = re.sub(pat, "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned


def generate_as(system_prompt: str, user_text: str, max_tokens: int = 480, temperature: float = 0.7) -> str:
    """
    Her çağrıda temiz context: create_chat_completion kullanıyoruz.
    """
    
    llm.reset()
    out = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        repeat_penalty=1.1,
    )
    text = out["choices"][0]["message"]["content"]
    return _clean(text)



def fintalk_discussion(news_text: str) -> Dict[str, str]:
    print("🧩 FinTalk simulation started...\n")

    messages = []

    selin_intro = generate_as(SYSTEM_MODERATOR, f"Open the discussion about: {news_text}.")
    messages.append(f"Selin: {selin_intro}")
    print("Moderator Intro:\n", selin_intro, "\n")

    bullish_view = generate_as(
        SYSTEM_BULLISH,
        f"The moderator introduced the topic: {news_text}. Respond with your opening bullish perspective."
    )
    messages.append(f"Bullish Investor: {bullish_view}")
    print("Bullish Investor:\n", bullish_view, "\n")

    bearish_view = generate_as(
        SYSTEM_BEARISH,
        f"The moderator introduced the topic: {news_text}. "
        f"The bullish economist said: {bullish_view}\n"
        "Now respond with your cautious analysis."
    )
    messages.append(f"Bearish Economist: {bearish_view}")
    print("Bearish Economist:\n", bearish_view, "\n")

    selin_wrap = generate_as(
        SYSTEM_MODERATOR,
        f"Based on the debate about {news_text}, summarize their main differences and close the panel politely."
    )
    messages.append(f"Selin: {selin_wrap}")
    print("Moderator Wrap-up:\n", selin_wrap, "\n")

    
    debate_text = "\n".join(messages)
    summary_prompt = (
        "Summarize this debate between a bullish and a bearish economist in 5 bullet points. "
        "Keep it grounded in the topic and add a balanced conclusion.\n\n"
        f"{debate_text}"
    )

    summary_resp = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert economic summarizer."},
            {"role": "user", "content": summary_prompt}
        ]
    )
    final_summary = summary_resp.choices[0].message.content.strip()
    print("📊 GPT Summary:\n", final_summary)

    return {
        "moderator_intro": selin_intro,
        "bullish_view": bullish_view,
        "bearish_view": bearish_view,
        "moderator_wrap": selin_wrap,
        "summary": final_summary
    }

def export_to_pdf(result: dict, filename="FinTalk_Report.pdf"):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []

    def add(title, text):
        story.append(Paragraph(f"<b>{title}</b>", styles["Heading3"]))
        story.append(Paragraph(text.replace("\n", "<br/>"), styles["BodyText"]))
        story.append(Spacer(1, 12))

    add("Topic", result.get("topic", "—"))
    add("Moderator Intro", result["moderator_intro"])
    add("Bullish Investor", result["bullish_view"])
    add("Bearish Economist", result["bearish_view"])
    add("Moderator Wrap-up", result["moderator_wrap"])
    add("GPT-4 Summary", result["summary"])

    story.append(Paragraph("<i>Generated by FinTalk – AI Economic Roundtable</i>", styles["Normal"]))
    doc.build(story)

async def generate_tts_files(result):
    voices = {
        "moderator_intro": "en-US-AriaNeural",
        "bullish_view": "en-US-GuyNeural",
        "bearish_view": "en-GB-RyanNeural",
        "moderator_wrap": "en-US-AriaNeural"
    }
    for key, voice in voices.items():
        filename = f"{key}.mp3"
        text = result[key]
        await edge_tts.Communicate(text, voice=voice, rate="+0%").save(filename)
        print(f"✅ {filename} oluşturuldu")


if __name__ == "__main__":
    topic = input("What's discussion topic ?\n>")
    result = fintalk_discussion(topic)
    result["topic"] = topic
    export_to_pdf(result)
    asyncio.run(generate_tts_files(result))
    
