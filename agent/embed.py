from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from . config import DATA_PATH, DOC_PATH, CHROMA

class Embedder:
    """
    Embeds documents from the ./documents directory using Ollama embeddings and stores them in a Chroma vector store.
    """
    def __init__(self):
        self.chroma = CHROMA

    def _get_existing_file_names(self) -> list:
        """
        Retrieves a list of all file names currently stored in the Chroma vector store.
        """
        if os.path.exists(DATA_PATH / "doc_lists.txt"):
            with open(DATA_PATH / "doc_lists.txt", "r") as f:
                file_names = f.read().splitlines()
        else:
            with open(DATA_PATH / "doc_lists.txt", "w") as f:
                pass
            file_names = []
        
        return file_names
    
    def _get_file_names(self) -> list:
        """
        Retrieves a list of all file names within a specified directory.
        Subdirectories are not traversed.
        """
        file_names = []
        for entry in os.listdir(DOC_PATH):
            full_path = os.path.join(DOC_PATH, entry)
            if os.path.isfile(full_path):
                file_names.append(entry)

        return file_names
    
    def _get_new_files(self) -> list:
        """
        Compares existing file names in the vector store with those in the documents directory
        to identify new files that need to be embedded.
        """
        existing_files = self._get_existing_file_names()
        current_files = self._get_file_names()
        
        new_files = [file for file in current_files if file not in existing_files]
        
        return new_files

    def embed_files(self):
        """
        Embeds new files found in the documents directory and adds them to the Chroma vector store.
        """
        print("[+] Checking for new files")
        new_files = self._get_new_files()
        
        if not new_files:
            print("[+] No new files to embed")
            return
        
        for file_name in new_files:
            print(f"[+] Embedding file: {file_name}")
            file_path = os.path.join(DOC_PATH, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if not content.strip():
                print(f"[-] File {file_name} is empty, skipping.")
                continue

            # TODO: Make this more robust
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_text(content)
            documents = [Document(page_content=text, metadata={"source": file_name}) for text in texts]
            self.chroma.add_documents(documents)
        
        with open(DATA_PATH / "doc_lists.txt", "a") as f:
            for file_name in new_files:
                f.write(file_name + "\n")