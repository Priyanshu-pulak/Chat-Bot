from pathlib import Path
from llama_index.core import (
    SimpleDirectoryReader, VectorStoreIndex, StorageContext,
    load_index_from_storage, Settings
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

DATA_FILE   = Path('extracted', 'pdf_text.txt')
PERSIST_DIR = Path('index_store')
PERSIST_DIR.mkdir(exist_ok=True)

llm = Ollama(
    model = "llama3", 
    request_timeout = 180.0,
    stream = False
)

embed_model = OllamaEmbedding(model_name="llama3")
Settings.llm = llm           
Settings.embed_model = embed_model

if not any(PERSIST_DIR.iterdir()):        # build the index once
    docs  = SimpleDirectoryReader(input_files=[str(DATA_FILE)]).load_data()
    index = VectorStoreIndex.from_documents(docs)   # uses local embeds
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:                                     # then just load it
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine(similarity_top_k=3)

print("Chatbot ready. Type 'exit' to quit.")
while True:
    q = input("You: ")
    if q.lower() in {"exit", "quit"}:
        break
    try:
        print("\nBot:", query_engine.query(q), "\n")
    except Exception as e:
        print("Error:", e, "\n")
