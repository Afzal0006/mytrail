import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from pymongo import MongoClient
import os

# ==== CONFIG ====
BOT_TOKEN = "8311824260:AAEXchUpld4AlE9Ifa1IPVOcj5sCG1KKLUo"
OWNER_ID = 6998916494  # yaha apna Telegram user id daalo (bot ke owner ka)

MONGO_URI = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # ya Mongo Atlas URI
DB_NAME = "telegram_bot"
COLLECTION_NAME = "subscriptions"

# ==== Mongo Setup ====
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
subscriptions = db[COLLECTION_NAME]

# ==== Messages ====
START_IMAGE = "https://i.ibb.co/Mk5jTp1s/x.jpg"
PREMIUM_IMAGE = "https://i.ibb.co/7tm7hNpf/x.jpg"

START_MESSAGE = (
    "Direct P#rn Video Channel 🌸\n\n"
    "D#si Maal Ke Deewano Ke Liye 😋\n\n"
    "No Sn#ps Pure D#si Maal 😙\n\n"
    "51000+ rare D#si le#ks ever.... 🎀\n\n"
    "Just pay and get entry...\n\n"
    "Direct video No Link - Ads Sh#t 🔥\n\n"
    "Price :- ₹69/-\n\n"
    "Validity :- lifetime"
)

PREMIUM_MESSAGE = (
    "𝗣𝗮𝘆 𝗝𝘂𝘀𝘁 ₹𝟲𝟵/- 𝗔𝗻𝗱 𝗚𝗲𝘁 𝗟𝗶𝗳𝗲𝘁𝗶𝗺𝗲 𝗔𝗰𝗰𝗲𝘀𝘀 🔥\n\n"
    "𝗦𝗲𝗻𝗱 𝗦𝗦 𝗮𝗳𝘁𝗲𝗿 𝗽𝗮𝘆𝗺𝗲𝗻𝘁🦋✅\n\n"
    "𝗦𝗘𝗡𝗗 𝗦𝗖𝗥𝗘𝗘𝗡𝗦𝗛𝗢𝗧 @MMSWALA069 💖"
)

# ==== Start Command ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")],
        [InlineKeyboardButton("🎥 Premium Demo", url="https://t.me/SexyEmoji")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(
        photo=START_IMAGE,
        caption=START_MESSAGE,
        reply_markup=reply_markup,
    )

# ==== Button Actions ====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "get_premium":
        keyboard = [
            [InlineKeyboardButton("🔙 Back", callback_data="back")],
            [InlineKeyboardButton("🎥 Premium Demo", url="https://t.me/SexyEmoji")]
        ]
        await query.edit_message_media(
            media={"type": "photo", "media": PREMIUM_IMAGE, "caption": PREMIUM_MESSAGE},
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")],
            [InlineKeyboardButton("🎥 Premium Demo", url="https://t.me/SexyEmoji")]
        ]
        await query.edit_message_media(
            media={"type": "photo", "media": START_IMAGE, "caption": START_MESSAGE},
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ==== Owner-only Commands ====
async def add_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ You are not allowed to use this command.")

    if not context.args:
        return await update.message.reply_text("Usage: /subscription {username}")

    username = context.args[0].lstrip("@")  # remove @ if present
    subscriptions.update_one({"username": username}, {"$set": {"username": username}}, upsert=True)

    await update.message.reply_text(f"✅ Subscription added for @{username}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ You are not allowed to use this command.")

    users = subscriptions.find()
    if users.count() == 0:
        return await update.message.reply_text("No subscriptions found.")

    text = "📊 Subscribed Users:\n\n"
    for u in users:
        text += f"@{u['username']}\n"

    await update.message.reply_text(text)

# ==== Main ====
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("subscription", add_subscription))
    app.add_handler(CommandHandler("stats", stats))

    print("Bot started successfully ✅")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    asyncio.run(main())
