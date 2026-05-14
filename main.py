from config.settings import settings
from core.chain import build_chain
from core.llm_factory import create_llm
from services.chat_service import ChatService
from ui.streamlit_app import run

llm = create_llm(settings)
chain = build_chain(llm)
service = ChatService(chain)

run(service)
