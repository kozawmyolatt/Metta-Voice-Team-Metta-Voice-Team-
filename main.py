import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# 1. Bot Token ကို Render ၏ Environment Variables မှ အလိုအလျောက် ယူမည်
TOKEN = os.getenv("TOKEN")

# Log ထုတ်ရန်
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# texts.txt ဖိုင်ထဲက စာများကို အလိုအလျောက် ဖတ်မည့် ပုံစံ
def load_text(section_name):
    try:
        with open("texts.txt", "r", encoding="utf-8") as f:
            content = f.read()
            return content
    except Exception as e:
        return "အချက်အလက် ရှာမတွေ့ပါ။"

# ၁။ /start နှိပ်လိုက်သည့်အခါ ခလုတ်များနှင့်အတူ မက်ဆေ့ပို့မည်
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌐 Metta Voice", callback_data="about_team")],
        [InlineKeyboardButton("🛠 လုပ်ဆောင်ချက်များ", callback_data="features")],
        [InlineKeyboardButton("📱 APK ဒေါင်းရန်", callback_data="apk_guide")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = load_text("WELCOME_TEXT")
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# ၂။ ခလုတ်တစ်ခုခုကို နှိပ်လိုက်သည့်အခါ texts.txt ထဲမှ စာများကို ပြန်ပြမည်
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about_team":
        text = load_text("ABOUT_TEAM")
        await query.message.edit_text(text)

    elif query.data == "features":
        text = load_text("FEATURES")
        await query.message.edit_text(text)

    elif query.data == "apk_guide":
        text = load_text("APK_GUIDE")
        await query.message.edit_text(text)

# ၃။ "apk" စာသားပါလာလျှင် ဖိုင်ပို့ပြီး ၅ မိနစ်နေလျှင် ပြန်ဖျက်မည့် ပုံစံ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_text = update.message.text.lower()

        if "apk" in user_text or "ဒေါင်းလုဒ်" in user_text:
            chat_id = update.effective_chat.id
            
            # Telegram ချန်နယ်မှ APK လင့်ခ်ကို ပို့မည်
            sent_msg = await context.bot.send_document(
                chat_id=chat_id,
                document="https://t.me/kozawmyolatt",
                caption="ဒါပါဗျာ၊ တောင်းထားတဲ့ APK ဖိုင်ပါ။"
            )
            
            # ၅ မိနစ် (စက္ကန့် ၃၀၀) စောင့်မည်
            await asyncio.sleep(300)
            
            # မက်ဆေ့ချ်ကို ပြန်ဖျက်မည်
            try:
                await context.bot.delete_message(
                    chat_id=chat_id,
                    message_id=sent_msg.message_id
                )
            except Exception as e:
                print(f"မက်ဆေ့ချ်ဖျက်ရာတွင် Error ဖြစ်သည်: {e}")

def main():
    if not TOKEN:
        print("Error: TOKEN environment variable is not set!")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot စတင်အလုပ်လုပ်နေပြီ...")
    application.run_polling()

if __name__ == '__main__':
    main()
