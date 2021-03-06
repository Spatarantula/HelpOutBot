from subprocess import call
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, filters
import requests
import os
from dotenv import load_dotenv

import json

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
volunOpList = []

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
    await update.message.reply_text("What field do you want to volunteer in?\n(/check to view your selected options)", reply_markup=reply_markup)

async def getVolunOp(update, context):
    query = update.callback_query
    await query.answer()
    ans = query.data
    if ans not in volunOpList:
        volunOpList.append(ans) 

async def checkOp(update, context):
    msg = ""
    for choice in volunOpList:
        msg += choice + ", "
    await update.message.reply_text(f"Your options are {msg}\n(/clear to delete options)\n(/done to confirm)")

async def clearOp(update, context):
    volunOpList.clear()

async def doneOp(update, context): # send to json
    if len(volunOpList) == 0:
        await update.message.reply_text("No options have been chosen!\n(/volunteer to start)")
        volunOp()
    else:
        await update.message.reply_text("Here are some sites to check out:")
        with open("volunteers.json") as f:
            volunteerChoices = json.load(f)
        for choice in volunOpList:
            if choice in volunteerChoices.keys():
                await update.message.reply_text(f"{choice.capitalize()}:")
                for urls in volunteerChoices[choice]:
                    await update.message.reply_text(f"{urls}")
                # print(f"{volunteerChoices[choice]}\n")
        volunOpList.clear()
        

# makes the bot
bot = ApplicationBuilder().token(BOT_TOKEN).build()

bot.add_handler(CommandHandler("volunteer", volunOp))
bot.add_handler(CallbackQueryHandler(getVolunOp))

bot.add_handler(CommandHandler("check", checkOp))
bot.add_handler(CommandHandler("clear", clearOp))
bot.add_handler(CommandHandler("done", doneOp))

bot.run_polling()
