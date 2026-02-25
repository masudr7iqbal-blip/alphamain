import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIGURATION ---
API_ID = 36701545
API_HASH = "92e8025812ade7acc47f9dc8057b34ad"
BOT_TOKEN = "8530900754:AAFiFRX60Om1r485mTSdiEs37rvvjz78NbI"
MONGO_URI = "mongodb+srv://Alpha:001100@cluster0.mp2hbsi.mongodb.net/?retryWrites=true&w=majority"
ADMIN_ID = 8303112705
ADMIN_LINK = "https://t.me/XpremiumB"
PHOTO_URL = "https://telegra.ph/file/70cc037b-7c6e-4cf2-babd-e6715bf8a80e.jpg"

# Database Setup
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo.AlphaBot
users_col = db.users

app = Client("AlphaPremiumBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def add_user(user_id):
    if not await users_col.find_one({"user_id": user_id}):
        await users_col.insert_one({"user_id": user_id})

@app.on_message(filters.command("start") & filters.private)
async def start(bot, message):
    await add_user(message.from_user.id)
    caption = (
        "**স্বাগতম! 👋**\n\n"
        "আমাদের **Alpha Premium** মেম্বারশিপে আপনি পাবেন ৩০০,০০০+ এক্সক্লুসিভ মিডিয়া ও নিয়মিত আপডেট। 💎\n\n"
        "👇 **প্যাকেজ ও পেমেন্ট ডিটেইলস নিচে দেখুন:**"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 ১ মাস প্যাকেজ — ৪৫০ টাকা 💎", callback_data="show_plans")],
        [InlineKeyboardButton("🔄 চেক রেগুলার আপডেট 🔔", url=ADMIN_LINK)],
        [InlineKeyboardButton("✅ পেমেন্ট ভেরিফিকেশন (ইনবক্স)", url=ADMIN_LINK)]
    ])
    await message.reply_photo(photo=PHOTO_URL, caption=caption, reply_markup=buttons)

@app.on_callback_query(filters.regex("show_plans"))
async def plans(bot, query):
    text = "**🔥 VIP MEMBERSHIP PLANS**\n\n✅ ১ মাস অ্যাক্সেস — ৪৫০ টাকা\n\n👇 **পেমেন্ট মেথড:**"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇧🇩 বিকাশ / নগদ", url=ADMIN_LINK), 
         InlineKeyboardButton("🇮🇳 UPI / Rupee", url=ADMIN_LINK)],
        [InlineKeyboardButton("💰 Binance ID: 1072071171", callback_data="binance")],
        [InlineKeyboardButton("✅ পেমেন্ট ভেরিফিকেশন (ইনবক্স)", url=ADMIN_LINK)]
    ])
    await query.message.edit_caption(caption=text, reply_markup=buttons)

@app.on_message(filters.photo & filters.user(ADMIN_ID))
async def make_post(bot, message):
    template_caption = (
        "🔞 **Exclusive Alpha VIP Access**\n\n🚀 **নতুন কন্টেন্ট আপলোড করা হয়েছে!**\n"
        "✅ Crystal Clear Ultra HD 4K\n✅ Fast & Private Support\n\n👇 **নিচের বাটন থেকে মেম্বারশিপ নিন:**"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🍿 Watch Free Demo", url=ADMIN_LINK)],
        [InlineKeyboardButton("💳 Buy Premium Subscription 💎", callback_data="show_plans")],
        [InlineKeyboardButton("✅ পেমেন্ট ভেরিফিকেশন (ইনবক্স)", url=ADMIN_LINK)]
    ])
    await message.reply_photo(photo=message.photo.file_id, caption=template_caption, reply_markup=buttons)

print("Alpha Premium Bot Live...")
app.run()
