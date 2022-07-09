from subprocess import call
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, filters
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
volunOpList = []

async def hello(update, context):
    await update.message.reply_text("G'day m'lady")
    
async def volunOp(update, context):
    keyboard = [
        [
                InlineKeyboardButton("Animals", callback_data="animals"), 
                InlineKeyboardButton("Children", callback_data="children"), 
                InlineKeyboardButton("Elderly", callback_data="elderly"),
        ],
        [
                InlineKeyboardButton("Community service", callback_data="community service"), 
                InlineKeyboardButton("Helping at events", callback_data="events"), 
                InlineKeyboardButton("Others", callback_data="others"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("What field do you want to volunteer in?\n (/check to confirm your options)", reply_markup=reply_markup)

async def getVolunOp(update, context):
    query = update.callback_query
    await query.answer()
    ans = query.data
    if ans not in volunOpList:
        volunOpList.append(ans) 

async def checkOp(update, context):
    await update.message.reply_text(f"Your options are {volunOpList}\nType /done to confirm")

#async def finalOp(update, context):
    
# makes the bot
bot = ApplicationBuilder().token(BOT_TOKEN).build()

# respond to /hi with function hello
bot.add_handler(CommandHandler("hi", hello))
bot.add_handler(CommandHandler("volunteer", volunOp))
bot.add_handler(CommandHandler("check", checkOp))
bot.add_handler(CallbackQueryHandler(getVolunOp))

bot.run_polling()