import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

# === TONE TEMPLATE ===
TONE_TEMPLATE = """
You are a warm, empathetic gut health coach. Speak in a friendly, supportive, and scientifically grounded tone.
Explain things simply, avoid jargon unless explained, and always offer actionable and kind guidance.

Examples of your tone:
- "It's okay — this happens to a lot of people."
- "Your concern is valid, and here's what we can look into."
- "Salads can cause bloating if your gut lining is irritated. You're not imagining it."

Now answer the following question:
"""

# === Load Mistral or similar model from HuggingFace ===
print("Loading model...")
model_id = "HuggingFaceH4/zephyr-7b-alpha"

tokenizer = AutoTokenizer.from_pretrained(model_id)

# Set pad_token if it doesn't exist
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.float16,
    resume_download=True
)
model.eval()
print("Model loaded.")

# === Load FAISS vector store ===
print("Loading FAISS vector store...")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

# === RAG-style answer function ===
def answer_query(query: str):
    print(f"Searching knowledge base for: {query}")
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)

    # Use Zephyr's chat template format
    messages = [
        {"role": "system", "content": TONE_TEMPLATE},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]
    
    # Apply chat template
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # Tokenize with length limit
    inputs = tokenizer(
        prompt, 
        return_tensors="pt", 
        truncation=True, 
        max_length=2048
    ).to(model.device)
    
    print("🤖 Generating response...")
    
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=200,  # Shorter response
            do_sample=True,
            temperature=0.6,     # Lower temperature
            top_p=0.8,          # Lower top_p
            top_k=40,           # Lower top_k
            repetition_penalty=1.15,  # Higher repetition penalty
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    # Decode only the new tokens
    new_tokens = output[0][inputs['input_ids'].shape[-1]:]
    answer = tokenizer.decode(new_tokens, skip_special_tokens=True)
    
    print("\nAnswer:\n")
    print(answer.strip())

# === Simple fallback function ===
def answer_query_simple(query: str):
    """Simpler version if the above still has issues"""
    print(f"🔍 Searching knowledge base for: {query}")
    docs = vectorstore.similarity_search(query, k=2)  # Fewer docs
    context = "\n\n".join(doc.page_content for doc in docs)

    # Very simple prompt
    prompt = f"Based on this information: {context[:500]}...\n\nQuestion: {query}\n\nAnswer:"
    
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(model.device)
    
    print("Generating response...")
    
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.5,
            top_p=0.7,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    new_tokens = output[0][inputs['input_ids'].shape[-1]:]
    answer = tokenizer.decode(new_tokens, skip_special_tokens=True)
    
    print("\nAnswer:\n")
    print(answer.strip())

# === Run interactively ===
if __name__ == "__main__":
    print("💡 If the main function fails, type 'simple' to use the fallback version")
    print()
    
    while True:
        query = input("\n Ask me a gut health question (or type 'exit'): ")
        if query.lower() in ['exit', 'quit']:
            break
        elif query.lower() == 'simple':
            query = input("Ask me a gut health question (simple mode): ")
            if query.lower() not in ['exit', 'quit']:
                try:
                    answer_query_simple(query)
                except Exception as e:
                    print(f"Error: {e}")
        else:
            try:
                answer_query(query)
            except Exception as e:
                print(f"Error: {e}")
                print("Try typing 'simple' for a simpler version")
