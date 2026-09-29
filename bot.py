import os

from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]

# Replies for each link command / button
REPLIES = {
    "youtube": "Youtube Link => https://www.youtube.com/kamikazie77",
    "linkedin": "LinkedIn URL => https://www.linkedin.com/in/dwaipayan-bandyopadhyay-007a/",
    "gmail": "Your gmail link here (I am not giving mine one for security reasons)",
    "geeks": "GeeksforGeeks URL => https://www.geeksforgeeks.org/",
}


def main_menu() -> InlineKeyboardMarkup:
    """Buttons shown under messages."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("YouTube", callback_data="youtube"),
            InlineKeyboardButton("LinkedIn", callback_data="linkedin"),
        ],
        [
            InlineKeyboardButton("Gmail", callback_data="gmail"),
            InlineKeyboardButton("GeeksforGeeks", callback_data="geeks"),
        ],
    ])


async def post_init(app: Application):
    """Registers the command list that appears in Telegram's Menu button."""
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("menu", "Show the button menu"),
        BotCommand("help", "List available commands"),
        BotCommand("youtube", "Get the YouTube URL"),
        BotCommand("linkedin", "Get the LinkedIn URL"),
        BotCommand("gmail", "Get the Gmail URL"),
        BotCommand("geeks", "Get the GeeksforGeeks URL"),
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello sir, Welcome to the Bot. Tap a button below or use /help.",
        reply_markup=main_menu(),
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choose an option:", reply_markup=main_menu())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available Commands :-\n"
        "/menu - Show the button menu\n"
        "/youtube - To get the youtube URL\n"
        "/linkedin - To get the LinkedIn profile URL\n"
        "/gmail - To get gmail URL\n"
        "/geeks - To get the GeeksforGeeks URL",
        reply_markup=main_menu(),
    )


def make_link_handler(key: str):
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(REPLIES[key])
    return handler


async def button_pressed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # stops the loading spinner on the button
    await query.message.reply_text(REPLIES[query.data])


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Sorry '{update.message.text}' is not a valid command")


async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Sorry I can't recognize you, you said '{update.message.text}'",
        reply_markup=main_menu(),
    )


def main():
    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .get_updates_connect_timeout(30)
        .get_updates_read_timeout(30)
        .get_updates_write_timeout(30)
        .get_updates_pool_timeout(30)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_command))
    for key in REPLIES:
        app.add_handler(CommandHandler(key, make_link_handler(key)))

    app.add_handler(CallbackQueryHandler(button_pressed))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))

    app.run_polling(bootstrap_retries=-1)


if __name__ == "__main__":
    main()