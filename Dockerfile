FROM python:3.14-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

FROM python:3.14-slim

WORKDIR /app

RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --ingroup app --no-create-home app

COPY --from=builder --chown=app:app /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH

COPY --chown=app:app . .

EXPOSE 8501

USER app

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

LABEL org.opencontainers.image.source=https://github.com/SeydinaBANE/chatBOT
LABEL org.opencontainers.image.description="Chatbot RAG avec Ollama + LangChain + Streamlit"
LABEL org.opencontainers.image.licenses=MIT

CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]
