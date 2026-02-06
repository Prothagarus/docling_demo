# %%
from docling.document_converter import DocumentConverter

# Initialize converter with default settings
converter = DocumentConverter()

# Convert the document into structured data
source_url = "https://arxiv.org/pdf/2408.09869"
result = converter.convert(source_url)

# Access structured data immediately
doc = result.document

print(doc.export_to_markdown())



#CHUNKING EXAMPLES
# %%
from docling.chunking import HierarchicalChunker
def print_chunk(chunk):
    print(f"Chunk length: {len(chunk.text)} characters")
    if len(chunk.text) > 30:
        print(f"Chunk content: {chunk.text[:30]}...{chunk.text[-30:]}")
    else:
        print(f"Chunk content: {chunk.text}")
    print("-" * 50)



# Process with HierarchicalChunker (structure-based)
hierarchical_chunker = HierarchicalChunker()
hierarchical_chunks = list(hierarchical_chunker.chunk(doc))

print(f"HierarchicalChunker: {len(hierarchical_chunks)} chunks")

# Print the first 3 chunks
for chunk in hierarchical_chunks[:5]:
    print_chunk(chunk)

# %%
from docling.chunking import HybridChunker

# Process with HybridChunker (token-aware)
hybrid_chunker = HybridChunker(max_tokens=1024, overlap_tokens=50)
hybrid_chunks = list(hybrid_chunker.chunk(doc))

print(f"HybridChunker: {len(hybrid_chunks)} chunks")

# Print the first 3 chunks
for chunk in hybrid_chunks[:5]:
    print_chunk(chunk)

# %%
## See https://codecut.ai/semantic-search-postgres-pgvector-ollama/ for postgres vector chunking

from docling.chunking import HybridChunker

# Initialize the chunker
chunker = HybridChunker(max_tokens=512, overlap_tokens=50)

# Create the chunks
rag_chunks = list(chunker.chunk(doc))

print(f"Created {len(rag_chunks)} intelligent chunks")

#VECTOR STORE CREATION
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# Create the vector store
texts = [chunk.text for chunk in rag_chunks]
vectorstore = FAISS.from_texts(texts, embeddings)

print(f"Built vector store with {len(texts)} chunks")



#RAGQUERY
# %%
query = "How does document processing work?"
relevant_docs = vectorstore.similarity_search(query, k=3)

print(f"Query: '{query}'")
print(f"Found {len(relevant_docs)} relevant chunks:")

for i, doc in enumerate(relevant_docs, 1):
    print(f"\nResult {i}:")
    print(f"Content: {doc.page_content[:150]}...")
# %%
