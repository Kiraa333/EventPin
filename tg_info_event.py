# Импортируем необходимые классы.
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

BOT_TOKEN = ''

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/info', '/site', '/review']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник проекта EventPin\n"
        "Я могу помочь вам:\n"
        "- Узнать о нашем проекте (/info)\n"
        "- Найти наш сайт (/site)\n"
        "- Оставить отзыв (/review)",
        reply_markup=markup
    )


async def help(update, context):
    await update.message.reply_text(
        "Я помогу вам ознакомиться с проектом EventPin.\n"
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/info - информация о проекте\n"
        "/site - ссылка на сайт\n"
        "/review - оставить отзыв или предложение\n"
        "/close - убрать клавиатуру")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )




async def site(update, context):
    await update.message.reply_text(
        "Сайт: our_url")


async def info(update, context):
    await update.message.reply_text(
        "EventPin - ваш путеводитель по миру интересных событий.\n\n"
        "• Находите интересные мероприятия рядом с вами\n"
        "• Открывайте для себя новые места и активности\n"
        "• Планируйте свой досуг легко и удобно\n\n"
        "EventPin – это удобство, стиль и яркие эмоции для всех!")


async def review(update, context):
    await update.message.reply_text(
        "Пожалуйста, поделитесь вашими впечатлениями о проекте EventPin.\n"
        "Напишите, что вам понравилось, а что можно улучшить.\n"
        "Ваши предложения очень важны для нас!\n\n"
        "Просто напишите ваше сообщение, и мы его обязательно рассмотрим.")


# Обработчик текстовых сообщений (для сбора отзывов)
async def handle_message(update, context):
    text = update.message.text
    user = update.message.from_user
    logger.info(f"Received feedback from {user.username} ({user.id}): {text}")

    # Сохраняем отзыв в файл
    with open("reviews.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user.username} (ID: {user.id})\nReview: {text}\n\n")

    await update.message.reply_text("Спасибо за ваш отзыв! Мы ценим ваше мнение и обязательно его рассмотрим.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("review", review))
    application.add_handler(CommandHandler("info", info))  # Добавлен обработчик для info

    # Добавляем обработчик текстовых сообщений (для отзывов)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
