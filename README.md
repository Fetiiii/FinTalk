# 📊 FinTalk — AI Economic Roundtable

**FinTalk** brings together two AI economists with different perspectives (Bullish & Bearish) in a moderated discussion format.

When a user submits a news article or economic topic, the system:
- 🎙️ Generates opinions from two AI economists
- 🧾 Creates a PDF report
- 🔊 Produces audio versions
- 📊 Provides GPT-powered summaries

## ✨ Features

- 🤖 **1 Moderator + 2 AI Economists:** Bullish & Bearish perspectives
- 🧠 **GPT-4 based summarization:** Intelligent analysis synthesis
- 📄 **PDF export:** Professional reports using ReportLab
- 🔊 **Text-to-Speech:** Audio versions via Edge TTS
- 🎨 **Gradio interface:** One-click user experience
- 🌍 **Multi-language support:** Discussion in multiple languages

> ⚠️ **Disclaimer:** This project is for educational and demonstration purposes only. Generated analyses are not investment advice.

---

## 📦 Table of Contents

- [Local Setup](#-local-setup)
  - [Requirements](#1️⃣-requirements)
  - [Environment Configuration](#2️⃣-environment-configuration)
  - [Download Model](#3️⃣-download-model)
  - [Run Application](#4️⃣-run-application)
- [Online Demo](#-online-demo)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Usage Examples](#-usage-examples)
- [Troubleshooting](#️-troubleshooting)
- [License](#-license)

---

## 💻 Local Setup

### 1️⃣ Requirements

```bash
pip install -r requirements.txt
```

**Required libraries:**
- openai
- gradio
- reportlab
- edge-tts
- llama-cpp-python
- huggingface-hub

### 2️⃣ Environment Configuration

Creating an `.env` file:

```env
API_KEY=sk-your-openai-api-key-here
```

### 3️⃣ Download Model

Download the Llama-3 Finance model (one-time setup):

```python
from huggingface_hub import hf_hub_download

hf_hub_download(
    repo_id="QuantFactory/Llama-3-8B-Instruct-Finance-RAG-GGUF",
    filename="Llama-3-8B-Instruct-Finance-RAG.Q4_K_S.gguf"
)
```
Or go to link and download manually-->(https://huggingface.co/QuantFactory/Llama-3-8B-Instruct-Finance-RAG-GGUF)

### 4️⃣ Run Application

Start the Gradio interface:

```bash
python app.py
```

Then open your browser.

---

## 🌐 Online Demo

Try the live demo on Hugging Face Spaces:

👉 **[FinTalk on Hugging Face Spaces](https://huggingface.co/spaces/fetii/FinTalk)**

*(The Space runs a lightweight version of the same system)*

---

## 🧩 How It Works

### Workflow

1. **User Input:** Submit economic news or topic
2. **AI Analysis:** 
   - Moderator introduces the topic
   - Bullish economist presents optimistic view
   - Bearish economist presents cautious view
3. **Synthesis:** GPT-4 generates comprehensive summary
4. **Output Generation:**
   - PDF report with all perspectives
   - Audio files for each economist
   - Visual summary in the interface

### AI Economists

| Role | Perspective | Focus |
|------|-------------|-------|
| 🎙️ **Moderator** | Neutral | Topic introduction and context |
| 📈 **Bullish Economist** | Optimistic | Growth opportunities and positive indicators |
| 📉 **Bearish Economist** | Cautious | Risks and potential challenges |

---

## 📁 Project Structure

```
FinTalk/
│
├── app.py                    # Main Gradio application
├── requirements.txt          # Python dependencies
├── .env                     # Your API keys (not in git)
│
├──Llama-3-8B-Instruct-Finance-RAG.Q4_K_S.gguf
│
└── README.md
```

---

## 📖 Usage Examples

### Example 1: Analyzing Fed Rate Decision

**Input:**
```
Federal Reserve announces 0.25% interest rate cut
```

**Output:**
- Bullish economist discusses economic stimulus benefits
- Bearish economist warns about inflation risks
- Moderator provides balanced context
- GPT summary synthesizes both views

### Example 2: Stock Market Analysis

**Input:**
```
Tech stocks rally as AI adoption accelerates
```

**Output:**
- Complete roundtable discussion
- PDF report with all arguments
- Audio recordings of each perspective
- Executive summary

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `OpenAI API error` | Check your API key in `.env` file |
| `Module not found` | Run `pip install -r requirements.txt` |
| `TTS generation fails` | Ensure `edge-tts` is properly installed |
| `PDF generation error` | Check `reportlab` installation and write permissions |

### Memory Issues

For large discussions or limited RAM:

```python
# In app.py, adjust model parameters
model_kwargs = {
    "n_ctx": 2048,  # Reduce context window
    "n_threads": 4   # Adjust thread count
}
```


## 📘 License

This project is released under the **MIT License**.

```
MIT License © 2025
```

Feel free to use, modify, and share.

---

## 🧠 Author's Note

**FinTalk** demonstrates the potential of AI-powered debate systems for educational purposes and perspective analysis.

The project combines natural language generation, speech synthesis, and document generation to create an interactive economic analysis tool.

---

## 📚 References

- **Llama 3 Model:** [Meta AI](https://ai.meta.com/llama/)
- **Finance-tuned Model:** [QuantFactory on Hugging Face](https://huggingface.co/QuantFactory/Llama-3-8B-Instruct-Finance-RAG-GGUF)
- **OpenAI GPT-4:** [OpenAI Platform](https://platform.openai.com/)
- **Gradio Framework:** [Gradio Documentation](https://www.gradio.app/)

---

<div align="center">

**⭐ Star this project if you find it interesting!**

For questions or feedback, feel free to open an [Issue](../../issues).

**Disclaimer:** This tool generates AI-based opinions for educational purposes only. Always consult professional financial advisors for investment decisions.

</div>
