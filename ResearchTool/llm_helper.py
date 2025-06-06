from enum import Enum

class LLM_MODEL_NAME(Enum):
    GEMINI = "gemini-1.5-flash"     # free tier today; paid tier not yet set :contentReference[oaicite:0]{index=0}
    GROK   = "grok-3-mini"          # “mini” is the low-cost option in xAI’s list :contentReference[oaicite:1]{index=1}
    GROQ   = "llama3-8b-8192"       # $0.05 / $0.08 per M tokens on GroqCloud :contentReference[oaicite:2]{index=2}
    OPENAI = "gpt-4.1-nano"         # $0.10 / $0.40 per M tokens—cheapest OpenAI text model :contentReference[oaicite:3]{index=3}
    OLLAMA = "llama3:8b"            # local 8-B Llama-3; no token cost (CPU/GPU only)

class LLM_BASE_URL(Enum):
    OPENAI_URL = "https://api.openai.com/v1"
    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta"
    GROK_URL = "https://api.x.ai/v1"
    GROQ_URL = "https://api.groq.com/openai/v1"
    OLLAMA_URL = "http://localhost:11434/v1"