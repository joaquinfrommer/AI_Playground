import ollama
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver 
from langgraph.config import get_stream_writer
from alive_progress import alive_bar
from . config import CHROMA, MODEL, SUMMARY_MODEL, SUMMARY_CLIENT, SYSTEM_PROMPT
from . utils import extract_visible_text

@tool
def ollama_web_search(query: str) -> str:
    """
    Search the internet for anything using Ollama's web search capability. 
    Use this tool to get up-to-date information to answer questions or to add context to other tool responses.

    Args:
        query (str): The search query.
    
    Returns:
        str: Formatted search results including titles, URLs, and content snippets.
    """
    summary_prompt = f"The following is a web search result.\n\
        If the title has to do with cybersecurity, hacking, or penetration testing, summarize the page along with any important commands, concepts, or tools mentioned.\n\
        If the title is a general topic, provide a brief summary of the content.\n\
        When summarizing, provide details that directly relate to the following - {query}. Here is the content:\n"
    
    writer = get_stream_writer()
    response = dict(ollama.web_search(query))
    result = ""
    for i, item in enumerate(response["results"]):
        html_text = extract_visible_text(item.get('content', ''))
        summary = SUMMARY_CLIENT.chat(
            model=SUMMARY_MODEL,
            messages=[
                {
                    "role":"user", 
                    "content": summary_prompt + f"Title: {item.get('title', "")} Content:" + html_text
                }
            ]
        )
        result += f"Result {i+1}:\nTitle: {item.get('title', "")}\nURL: {item.get('url', "")}\nContent: {summary.message.content}\n\n"
    
    writer("Web Search Results:\n" + result)
    return result.strip()

def retriever(query: str) -> str:
    """
    Searches through a vast collection of documents to find relevant information based on the user's query.
    Use this tool to find specific details and information based on the user's input.
    You should synthesize the information from the retrieved documents to provide a comprehensive answer.
    If no relevant information is found, state that there was nothing relevant in the vector store.

    Args:
        query (str): A query to search the vector store.
    
    Returns:
        str: The content of the retrieved documents.    
    """
    #TODO: k = num docs to retrieve, fetch_k = num docs to fetch initially
    retriever = CHROMA.as_retriever(search_kwargs={"k": 5})
    # TODO: Find out how to get the model to answer my prompt based on the retrieved documents
    docs = retriever.invoke(query)

    return "\n\n".join([doc.page_content for doc in docs])

class AgentRunner:
    """
    Allows users to interact with agent
    """
    def __init__(self):
        # TODO: Adjust system prompt
        self.agent = create_agent(
            model=MODEL,
            tools=[retriever, ollama_web_search],
            system_prompt=SYSTEM_PROMPT,
            checkpointer=InMemorySaver()
        )

    def interact(self):
        """
        Main agent loop
        """
        print("Offsec Agent - Happy Pwning :)\n" + "="*20)
        while True:
            query = input("> ")
            if query.lower() == 'exit':
                print("Got Root?")
                break

            print("Agent\n" + "="*20)
            # TODO: Streaming not showing tool calls
            with alive_bar(bar=None, title="Thinking", spinner="dots_waves") as bar:
                for chunk in self.agent.stream(  
                    {"messages": [{"role": "user", "content": f"{query}"}]},
                    stream_mode="updates",
                    config={"configurable": {"thread_id": "1"}}
                ):
                    for step, data in chunk.items():
                        print(f"step: {step}")
                        for content in data['messages'][-1].content_blocks:
                            print(content.get('text', ''))