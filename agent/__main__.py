import dotenv
dotenv.load_dotenv()

from . embed import Embedder
from . agent import AgentRunner

def main():
    embedder = Embedder()
    embedder.embed_files()
    runner = AgentRunner()
    runner.interact()

if __name__ == "__main__":
    main()