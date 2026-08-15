FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
# Голосовые копируются в образ, чтобы он работал и без compose.
# В docker-compose.yml поверх монтируется папка ./voices с сервера.
COPY voices/ ./voices/

RUN useradd --create-home --uid 1000 bot
USER bot

CMD ["python", "bot.py"]
