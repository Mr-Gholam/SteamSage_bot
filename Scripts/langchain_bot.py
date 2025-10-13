from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from Scripts.recommender import collaborative

# 🔹 Initialize Ollama LLM (make sure Ollama is running and model is pulled, e.g., "llama2" or "mistral")
llm = Ollama(model="llama3.2")  # You can change "llama2" to any other Ollama model you have

# Prompt template for LangChain
prompt = ChatPromptTemplate.from_template("""
You are GameBot, a friendly gaming assistant.
If the user asks for game suggestions, use your knowledge and the function recommend_games().
Be concise and conversational.

User: {user_input}
""")

def chat_with_langchain(user_input: str):
    
    if "recommend" in user_input.lower():
        cleaned_input = user_input.lower().replace("recommend", "", 1).strip()
        recs = collaborative(cleaned_input)
        return "🎮 Try these games:\n• " + "\n• ".join(recs)

    # Otherwise, use Ollama LLM via LangChain
    chain = prompt | llm
    return chain.invoke({"user_input": user_input})