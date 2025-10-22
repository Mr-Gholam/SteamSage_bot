from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from Scripts.recommender import collaborative, hybrid, content_based
import re

# 🔹 Initialize Ollama LLM (make sure Ollama is running and model is pulled, e.g., "llama2" or "mistral")
llm = OllamaLLM(model="llama3.2")

# Prompt template for LangChain
prompt = ChatPromptTemplate.from_template("""
You are GameBot, a friendly gaming assistant.
If the user asks for game suggestions, use your knowledge and the function recommend_games().
Be concise and conversational.

User: {user_input}
""")


def recommend_game(user_input, triggers):
    # Method selection
    method_map = {
        "hybrid": (hybrid, "Hybrid"),
        "collaborative": (collaborative, "Collaborative"),
        "content": (content_based, "Content-based"),
        "content-based": (content_based, "Content-based"),
    }
    method = "hybrid"
    for m in method_map:
        if re.search(rf"\b{m}\b", user_input, re.IGNORECASE):
            method = m
            break
    cleaned_input = user_input
    helpers = [r"using", r"with", r"by"]
    for trig in triggers + helpers + list(method_map.keys()):
        cleaned_input = re.sub(trig, "", cleaned_input, flags=re.IGNORECASE)
    cleaned_input = cleaned_input.strip()
    rec_func, method_label = method_map[method]
    recs = rec_func(cleaned_input)
    if recs:
        return (
            "🎮 Try these games:\n• "
            + "\n• ".join(recs)
            + f"\nRecommendation created by {method_label}()"
        )
    else:
        return f"Sorry, I couldn't find any recommendations for your query (method: {method_label})."


def chat_with_langchain(user_input: str):
    # Triggers for recs
    triggers = [
        r"recommend",
        r"suggest",
        r"give me",
        r"find me",
        r"any good",
        r"what should i play",
        r"game for me",
    ]

    if any(re.search(trig, user_input, re.IGNORECASE) for trig in triggers):
        return recommend_game(user_input, triggers)

    # Otherwise, use LLM for regular chat
    chain = prompt | llm
    return chain.invoke({"user_input": user_input})


