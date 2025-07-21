from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama

# Initialisation du modèle Ollama
llm = ChatOllama(model="tinyllama")

# Prompt basique : le chatbot répond à la question
template = """Tu es un assistant utile. Réponds simplement à la question suivante :

Question: {question}

Réponse:"""

prompt = PromptTemplate(input_variables=["question"], template=template)
chat_chain = LLMChain(llm=llm, prompt=prompt)

def poser_question(question: str) -> str:
    reponse = chat_chain.run(question)
    return reponse
