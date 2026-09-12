import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ခင်ဗျားရဲ့ Bot Token ထည့်ရန်
TOKEN = "8922583776:AAHfW5xnOFwzh2yU9vySlowtMOPHsK-lVls"

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
        
        sections = content.split("[")
        for sec in sections:
            if sec.startswith(section_name + "]"):
                return sec.split("]", 1)[1].strip()
    except Exception as e:
        print(f"ဖိုင်ဖတ်ရာတွင် အမှားဖြစ်သည်: {e}")
    
    return "အချက်အလက် ရှာမတွေ့ပါ။"

# ၁။ /start နှိပ်လိုက်သည့်အခါ ခလုတ်များနှင့်အတူ မီနူပြခြင်း
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👥 Metta Voice Team အကြောင်း", callback_data="about_team")],
        [InlineKeyboardButton("🚀 လုပ်ဆောင်ချက်များနှင့် ရည်ရွယ်ချက်", callback_data="features")],
        [InlineKeyboardButton("📥 APK တောင်းယူရန် လမ်းညွှန်", callback_data="apk_guide")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = load_text("WELCOME_TEXT")
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# ၂။ ခလုတ်တစ်ခုခုကို နှိပ်လိုက်သည့်အခါ texts.txt ထဲက စာကို လှမ်းထုတ်ပြခြင်း
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "about_team":
        text = load_text("ABOUT_TEAM")
        await query.message.edit_text(text, parse_mode="Markdown")
        
    elif query.data == "features":
        text = load_text("FEATURES")
        await query.message.edit_text(text, parse_mode="Markdown")
        
    elif query.data == "apk_guide":
        text = load_text("APK_GUIDE")
        await query.message.edit_text(text, parse_mode="Markdown")

# ၃။ "apk" စာသားပါလာရင် ဖိုင်ပို့ပြီး ၅ မိနစ်နေရင် ပြန်ဖျက်မည့် ပုံစံ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_text = update.message.text.lower()
        
        if "apk" in user_text or "အေပီကေ" in user_text:
            chat_id = update.effective_chat.id
            
            # Telegram ချန်နယ်က APK လင့်ခ်ကို ထည့်သွင်းထားသည်
            sent_msg = await context.bot.send_document(
                chat_id=chat_id,
                document="https://t.me/kozawmyolatt200118/31",
                caption="ဒါပါဗျာ၊ တောင်းထားတဲ့ APK ဖိုင်ပါ။ (ဒီစာနဲ့ဖိုင်ဟာ ၅ မိနစ်ပြည့်ရင် အလိုအလျောက် ပျောက်သွားပါမယ်။)"
            )
            
            # ၅ မိနစ် (စက္ကန့် ၃၀၀) စောင့်မည်
            await asyncio.sleep(300) 
            
            # မက်ဆေ့ချ်ကို ပြန်ဖျက်မည်
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=sent_msg.message_id)
            except Exception as e:
                print(f"မက်ဆေ့ချ်ဖျက်ရာတွင် အမှားဖြစ်သွားသည်: {e}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex("^/start$"), start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    application.run_polling()

if __name__ == '__main__':
    main()
