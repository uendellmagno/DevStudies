import logging
from urllib.parse import quote
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
LANGUAGE, NAME, REQUEST = range(3)
GROUP_ID = -1002373442443  # Replace with your group ID

# Translation dictionary
MESSAGES = {
    'ptbr': {
        'welcome': '👋 Bem-vindo à AVLI Solutions! Por favor, escolha seu idioma:',
        'name_prompt': 'Por favor, compartilhe seu nome.',
        'thanks_name': '👍 Obrigado {name}! Qual serviço ou solução você está procurando?',
        'confirmation': '✅ Obrigado! Recebemos sua solicitação e entraremos em contato em breve.\n\nNosso tempo médio de resposta é de 1-2 horas úteis.',
        'error': '⚠️ Oops! Ocorreu um erro. Por favor, tente novamente mais tarde.',
        'cancel': '❌ Operação cancelada. Use /start para começar novamente.',
    },
    'en': {
        'welcome': '👋 Welcome to AVLI Solutions! Please choose your language:',
        'name_prompt': 'Please share your name.',
        'thanks_name': '👍 Thanks {name}! What service or solution are you looking for?',
        'confirmation': '✅ Thank you! We\'ve received your request and will contact you shortly.\n\nOur typical response time is 1-2 business hours.',
        'error': '⚠️ Oops! Something went wrong. Please try again later.',
        'cancel': '❌ Operation cancelled. Use /start to begin again.',
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initiate conversation and present language options."""
    keyboard = [
        [
            InlineKeyboardButton("🇧🇷 Português", callback_data='ptbr'),
            InlineKeyboardButton("🇺🇸 English", callback_data='en'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        MESSAGES['ptbr']['welcome'],  # Default PTBR welcome message
        reply_markup=reply_markup
    )
    return LANGUAGE


async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the selected language and ask for name."""
    query = update.callback_query
    await query.answer()

    selected_lang = query.data
    context.user_data['lang'] = selected_lang

    lang_data = MESSAGES.get(selected_lang, MESSAGES['ptbr'])
    await query.edit_message_text(text=f"{lang_data['welcome']}\n\n{lang_data['name_prompt']}")
    return NAME


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store name and ask for request."""
    lang = context.user_data.get('lang', 'ptbr')
    lang_data = MESSAGES.get(lang, MESSAGES['ptbr'])

    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        lang_data['thanks_name'].format(name=update.message.text)
    )
    return REQUEST


async def receive_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process data and send to support group."""
    try:
        user = update.message.from_user
        lang = context.user_data.get('lang', 'ptbr')
        lang_data = MESSAGES.get(lang, MESSAGES['ptbr'])

        # Collect data
        provided_name = context.user_data.get('name', 'Not provided')
        user_request = context.user_data.get('request', update.message.text)
        chat_id = update.effective_chat.id

        # Generate user link
        user_link = f"https://t.me/{user.username}" if user.username else "Not available"

        # Create conversation link
        start_param = quote(f'Hi! We received your request: "{user_request}". How can we assist you?')
        conversation_link = f"{user_link}?start={start_param}"

        # Format group message (remains untranslated)
        formatted_message = (
            f"🆕 New Request\n\n"
            f"👤 Telegram Name: {user.full_name}\n"
            f"🧑 Provided Name: {provided_name}\n"
            f"🏷️ User Link: {user_link}\n"
            f"🆔 User ID: {chat_id}\n\n"
            f"💬 Chat Link: {conversation_link}\n\n"
            f"📝 Request: {user_request}"
        )

        # Send to support group
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=formatted_message
        )

        # Confirm receipt to user
        await update.message.reply_text(lang_data['confirmation'])

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(lang_data.get('error', MESSAGES['ptbr']['error']))
    finally:
        context.user_data.clear()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the current conversation."""
    lang = context.user_data.get('lang', 'ptbr')
    lang_data = MESSAGES.get(lang, MESSAGES['ptbr'])

    await update.message.reply_text(lang_data['cancel'])
    context.user_data.clear()
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    application = Application.builder().token("7767112485:AAHR-k7qE7EN7Oph0hul5yPd5Z3kxoq-i3A").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [CallbackQueryHandler(select_language)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            REQUEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_request)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()