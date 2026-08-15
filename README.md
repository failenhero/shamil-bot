# shamil-bot

Телеграм-бот, который кидает случайное голосовое из папки `voices/`, когда его
упоминают через `@` или когда сообщение начинается с `Шамиль,`.

## 1. Создать бота в @BotFather

1. `/newbot` → имя → username (должен заканчиваться на `bot`) → получите токен.
2. `/setprivacy` → выбрать бота → **Disable**.
   Без этого бот видит только сообщения с упоминанием, и триггер `Шамиль,` не сработает.
3. Добавить бота в группу. Если privacy выключили уже после добавления —
   удалить бота из группы и добавить заново.

## 2. Развернуть на сервере

Docker Engine (если ещё не стоит):

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER   # затем перелогиниться, чтобы docker работал без sudo
```

Код и запуск:

```bash
sudo mkdir -p /opt/shamil-bot && sudo chown $USER:$USER /opt/shamil-bot
git clone https://github.com/failenhero/shamil-bot.git /opt/shamil-bot
cd /opt/shamil-bot

cp .env.example .env
nano .env          # вписать BOT_TOKEN, ALLOWED_CHAT_IDS пока оставить пустым
chmod 600 .env

docker compose up -d --build
docker compose logs -f
```

Порты открывать не нужно: бот работает через long polling, только исходящие
соединения. Домен и TLS тоже не нужны.

## 3. Ограничить бота своими группами

С пустым `ALLOWED_CHAT_IDS` бот отвечает в любом чате. Чтобы ограничить:

1. Напишите что-нибудь в своей группе.
2. В `docker compose logs -f` найдите строку `[LOG] ВСЕ сообщения: ... в чате -100...`
3. Впишите этот ID в `.env` (несколько — через запятую) и перезапустите:

```bash
docker compose restart
```

## Эксплуатация

| Действие | Команда |
|---|---|
| Логи | `docker compose logs -f` |
| Статус | `docker compose ps` |
| Перезапуск | `docker compose restart` |
| Остановить | `docker compose down` |
| Обновить код | `git pull && docker compose up -d --build` |
| Добавить голосовые | положить `.ogg` в `voices/` — пересборка не нужна |

Контейнер стартует сам после перезагрузки сервера (`restart: unless-stopped`).

## Конфигурация

Всё в `.env`, см. `.env.example`:

- `BOT_TOKEN` — токен от @BotFather, обязателен.
- `ALLOWED_CHAT_IDS` — ID чатов через запятую. Пусто = работать везде.
