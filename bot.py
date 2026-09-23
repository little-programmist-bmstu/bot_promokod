import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from database import get_promo_code_by_key

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print(
        "[!] Не задан BOT_TOKEN.",
        file=sys.stderr,
    )
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("promo-bot")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

START_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/start")]],
    resize_keyboard=True,
)


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "👋 Привет! Я бот для выдачи промокодов от партнёров мероприятия.\n\n"
        "Если ты был на мероприятии и получил уникальный ключ — "
        "просто отправь его мне сообщением, и я выдам промокод.\n\n"
        "📌 Формат ключа: EVENT-KEY-XXX\n"
        "Пример: EVENT-KEY-001\n",
        reply_markup=START_KB,
    )


@dp.message(F.text)
async def handle_key(message: Message) -> None:
    """
    Принимает любой текст от пользователя и пытается найти по нему промокод.
    """
    user_input = message.text.strip()
    log.info("Пользователь %s ввёл: %r", message.from_user.id, user_input)

    try:
        promo = get_promo_code_by_key(user_input)
    except Exception as e:
        log.exception("Ошибка при выполнении SQL-запроса: %s", e)
        await message.answer(
            "⚠️ Произошла ошибка при обработке ключа. "
            "Попробуй ещё раз или обратись к организаторам."
        )
        return

    if promo is None:
        await message.answer(
            "❌ Ключ не найден. Проверь, что ты ввёл ключ в формате "
            "EVENT-KEY-XXX, и попробуй снова."
        )
        return

    await message.answer(
        f"🎉 Поздравляем! Твой промокод от партнёра мероприятия:\n\n"
        f"    <code>{promo}</code>\n\n"
        f"Покажи этот код на кассе партнёра или введи в личном кабинете "
        f"их сайта, чтобы получить скидку.",
        parse_mode="HTML",
    )


async def main() -> None:
    log.info("Бот запускается…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Бот остановлен")