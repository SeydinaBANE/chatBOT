from langchain_core.prompts import ChatPromptTemplate


def build_chat_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant utile. Réponds en français de manière claire et concise."),
        ("human", "{question}"),
    ])
