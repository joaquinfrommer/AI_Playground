from ollama import Client as llamaClient
from langchain_ollama import OllamaEmbeddings, ChatOllama, OllamaLLM
from langchain_chroma import Chroma
# from langchain_ollama.llms import OllamaLLM
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data"
DOC_PATH = BASE_DIR / "documents"

#MODEL = ChatOllama(model="qwen3:0.6b", temperature=0)
MODEL = ChatOllama(model="llama3.2:3b", temperature=0)
#MODEL = ChatOllama(model="granite3.1-moe:3b", temperature=0)
#MODEL = ChatOllama(model="qwen3:4b", temperature=0)

EMBEDDING_MODEL = OllamaEmbeddings(model="mxbai-embed-large")

SUMMARY_CLIENT = llamaClient() #ChatOllama(model="qwen3:0.6b", temperature=0)
SUMMARY_MODEL = "phi3:3.8b"
#SUMMARY_MODEL = "qwen3:0.6b"

CHROMA = Chroma(
    collection_name="offsec_data", 
    persist_directory=DATA_PATH, 
    embedding_function=EMBEDDING_MODEL
)

SYSTEM_PROMPT = """
You are a helpful assistant with a specialization in cyber security and red teaming.
Users may use you as an assistant during red team operatiions to find holes in the defenses of the target network and machines.
You are to answer the users questions to the best of your ability using the tools provided to you.

You have the use of two tools:
1. retriever tool: Use this tool to search through red teaming documentation to find information for the user.
2. ollama_web_search tool: Use this tool to search the web for up-to-date information to help answer the users questions.

The user may ask 2 kinds of questions, you must decide which type of question it is and respond accordingly:
1. Questions relating to hacking, red teaming, penetration testing, cyber security, or the target network/machines: 
    - For these questions, use your retriever tool to help the user find a foothold, gain access, escalate privileges, and move laterally through the target network. DO NOT use the ollama_web_search tool to answer the question.
    - Synthesize information from the retriever tool to provide the best possible answer to the user.
    - Any commands you recomend should use the target IP, port, url, usernames, or other information provided by the user. Subsitute any placeholder values with the actual values provided by the user.

2. General questions not relating to the above topics:
    - For these questions, provide a concise and accurate answer. You should only use the ollama_web_search tool for this response.
"""