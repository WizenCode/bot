#!/usr/bin/python
# -*- coding: utf-8 -*-
#In the name of God
import os
import sys
import json
import random
import urllib
import urllib2
import telebot
import redis as r
from time import sleep
import requests as req
from telebot import util
from telebot import types
from random import randint
from termcolor import colored
from urllib import urlretrieve as download
reload(sys)
sys.setdefaultencoding("utf-8")
################################################################################
api_token = "524110905:AAFDn4g3MS8vVPsp1T6-2YW84CLk6znQPXI" #Token must be here...
sudos = [
    478026278,
    0
] #Sudo users is must be here...
channel = "winey" #Channel id without @
sudo_username = "princedard" #Sudo username without @
payment_link = "https://idpay.ir/princedell" #Your payment link
################################################################################
redis = r.StrictRedis(host="localhost" , port=6379)
print colored("Getting token..." , "yellow")
bot = telebot.TeleBot(api_token)
print colored("Bot is online now!" , "green")
################################################################################
def lock_text(m , u):
    isadded = redis.sismember("groups" , m)
    isadmin = str(redis.sismember("group-{}".format(m) , "{}".format(u)))
    if isadded=="True" and userid in sudos or isadmin=="True":
        if str(redis.sismember("lock_text" , m))=="True":
            return "🔐"
        else:
            return "🔓"
def lock_photo(m , u):
    isadded = redis.sismember("groups" , m)
    isadmin = str(redis.sismember("group-{}".format(m) , "{}".format(u)))
    if isadded=="True" and userid in sudos or isadmin=="True":
        if str(redis.sismember("lock_photo" , m))=="True":
            return "🔐"
        else:
            return "🔓"
def lock_video(m , u):
    isadded = redis.sismember("groups" , m)
    isadmin = str(redis.sismember("group-{}".format(m) , "{}".format(u)))
    if isadded=="True" and userid in sudos or isadmin=="True":
        if str(redis.sismember("lock_video" , m))=="True":
            return "🔐"
        else:
            return "🔓"
#######################################################################################################################################################################
@bot.message_handler(commands=['start'])
def starting(m):
    userid = m.from_user.id
    chatid = m.chat.id
    redis.sadd("members" , "{}".format(userid))
    markup = types.InlineKeyboardMarkup()
    link = types.InlineKeyboardButton(text="برنامه نویس🍃" , url="https://t.me/{}".format(sudo_username))
    channel_link = types.InlineKeyboardButton(text="کانال ما🍃" , url="https://t.me/{}".format(channel))
    markup.add(link , channel_link)
    bot.send_message( chatid , """
🌟به ربات آنتی اسپم {} خوش اومدی...

🐍برنامه نویسی شده به زبان قدرتمند پایتون :)
💎پرسرعت بسیار بالا در پردازش ، قدرتمند در مدیریت و بی همتا در حفاظت از گروه شما...

📌جهت فعالسازی ربات باید از طریق [درگاه پرداخت ما]({}) ربات را خریداری کرده و با گرفتن اسکرین شات از فاکتور پرداخت خود ، آن را در [چت خصوصی مدیر](https://telegram.me/{}) ربات ارسال کنید!
_🌹لینک گروه خود را نیز در همان چت ارسال نمایید._
""".format(bot.get_me().first_name , payment_link , sudo_username) , parse_mode="Markdown" , reply_markup=markup)
#######################################################################################################################################################################
@bot.message_handler(commands=['ping'])
def ping(m):
    userid = m.from_user.id
    chatid = m.chat.id
    bot.send_message(chatid , "🐍انلاینم بخدا")
#######################################################################################################################################################################
@bot.message_handler(commands=['promote'])
def promote(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    replied = m.reply_to_message
    isadded = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    if chattype == "supergroup" and isadded=="False" and userid in sudos and replied:
        redis.sadd("group-{}".format(chatid) , "{}".format(userid))
        bot.send_message(chatid , "✨کاربر مورد نظر ارتقا رتبه یافت!")
    elif chattype == "supergroup" and isadded=="True" and userid in sudos and replied:
        bot.send_message(chatid , "✨کاربر مورد نظر از قبل دارای مقام بود!")
#######################################################################################################################################################################
@bot.message_handler(commands=['demote'])
def demote(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    replied = m.reply_to_message
    isadded = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    if chattype == "supergroup" and isadded=="True" and userid in sudos and replied:
        redis.srem("group-{}".format(chatid) , "{}".format(userid))
        bot.send_message(chatid , "🥀کاربر مورد نظر تنزل رتبه یافت!")
    elif chattype == "supergroup" and isadded=="False" and userid in sudos and replied:
        bot.send_message(chatid , "🥀کاربر مورد نظر دارای مقام نبود!")
#######################################################################################################################################################################
@bot.message_handler(commands=['add'])
def add(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    if chattype == "supergroup" and isadded=="False" and userid in sudos:
        redis.sadd("groups" , "{}".format(chatid))
        bot.send_message(chatid , "🍃سوپرگروه با موفقیت به لیست گروه های تحت پشتیبانی افزوده شد!")
    elif chattype == "supergroup" and isadded=="True" and userid in sudos:
        bot.send_message(chatid , "🍃سوپرگروه در حال حاضر در لیست گروه های تحت پشتیبانی موجود میباشد!")
#######################################################################################################################################################################
@bot.message_handler(commands=['rem'])
def rem(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    if chattype == "supergroup" and isadded=="True" and userid in sudos:
        redis.srem("groups" , "{}".format(chatid))
        bot.send_message(chatid , "🍂سوپرگروه با موفقیت از لیست گروه های تحت پشتیبانی محروم گردید!")
    elif chattype == "supergroup" and isadded=="False" and userid in sudos:
        bot.send_message(chatid , "🍂سوپرگروه در حال حاضر در لیست گروه های تحت پشتیبانی ثبت نشده است!")
#######################################################################################################################################################################
@bot.message_handler(commands=['info'])
def info(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    if chattype == "supergroup" and isadded=="True":
        if userid in sudos:
            rank = "🥇مالک ربات"
        elif isadmin=="True":
            rank = "🥈مدیر گروه"
        else:
            rank = "🥉کاربر عادی"
        bot.send_message(chatid , """
👤شناسه شما : {}
👥شناسه گروه : {}
🍁مقام شما : {}
""".format(userid , chatid , rank))
#######################################################################################################################################################################
@bot.message_handler(commands=['help'])
def help(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    markup = types.InlineKeyboardMarkup()
    link = types.InlineKeyboardButton(text="برنامه نویس🍃" , url="https://t.me/{}".format(sudo_username))
    channel_link = types.InlineKeyboardButton(text="کانال ما🍃" , url="https://t.me/{}".format(channel))
    markup.add(link , channel_link)
    if chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True":
        bot.send_message(chatid , """
📖راهنمای دستورات ربات برای مدیران :

🔐 [/]lock `( photo | video | gif | sticker | music | voice | location | contact | tgservice | text | caption | link | forward | filters | join | game )`
🔓 [/]unlock `( photo | video | gif | sticker | music | voice | location | contact | tgservice | text | caption | link | forward | filters | join | game )`
⚜️ [/]settings
🔰 [/]modlist

🔇 [/]muteall
🔈 [/]unmuteall

🚫 [/]ban ( reply )
✅ [/]unban ( reply )
⚜️ [/]banlist
❌ [/]kickme

📜 [/]set ( welcome | link | rules )
➖ [/]clear ( banlist | link | rules)

🌐 [/]link

🚸 [/]welcome enable
❗️ [/]welcome disable

📂 [/]addfilter {TEXT}
📄 [/]remfilter {TEXT}
🗂 [/]filterlist

🏷 [/]info
""" , reply_markup=markup)
#######################################################################################################################################################################
@bot.message_handler(commands=['kickme'])
def kickme(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    seconds = 3
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    if chattype == "supergroup" and isadded=="True":
        bot.send_message(chatid , "🍃کاربر {} به دستور خود در {} ثانیه اینده اخراج خواهد شد!".format(userid , seconds))
        time.sleep(seconds)
        bot.kick_chat_member(chatid , userid)
#######################################################################################################################################################################
@bot.message_handler(commands=['addfilter'])
def addfilter(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    isword = str(redis.sismember("filter-{}".format(chatid) , wordd))
    if chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True" and isword=="False":
		t = m.text.replace('/addfilter ','')
        redis.sadd("filter-{}".format(chatid) , t)
        bot.send_message(chatid , "🍃عبارت {} با موفقیت به لیست عبارات غیرمجازی افزوده شد!".format(text))
    elif chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True" and isword=="True":
        bot.send_message(chatid , "🍃عبارت مورد نظر از قبل در لیست موجود بود!")
#######################################################################################################################################################################
@bot.message_handler(commands=['remfilter'])
def remfilter(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    isword = str(redis.sismember("filter-{}".format(chatid) , wordd))
    if chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True" and isword=="True":
		t = m.text.replace('/remfilter ','')
        redis.srem("filter-{}".format(chatid) , t)
        bot.send_message(chatid , "🍂عبارت {} با موفقیت از لیست عبارات غیرمجازی حذف گردید!".format(text))
    elif chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True" and isword=="False":
        bot.send_message(chatid , "🍂عبارت مورد نظر از قبل در لیست موجود نبود!")
#######################################################################################################################################################################
@bot.message_handler(commands=['filterlist'])
def filterlist(m):
    text = m.text
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    words = redis.smembers("filter-{}".format(chatid))
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    filterlist = "🍃لیست عبارات غیرمجاز گروه شما:\n\n"
    i = 0
    if chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True":
        for a in words:
            i = i + 1
            filterlist = str(filterlist) + str(i) + " - " + str(a) + "\n"
        bot.send_message(chatid , filterlist)
#######################################################################################################################################################################
@bot.message_handler(commands=['modlist'])
def modlist(m):
    text = m.text
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    mods = redis.smembers("group-{}".format(chatid))
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    midlost = "📜لیست مدیران گروه شما :\n\n"
    i = 0
    if chattype == "supergroup" and isadded=="True":
        for m in mods:
            i = i + 1
            modlist = str(modlist + i + " - " + m + "\n")
        bot.send_message(chatid , modlist)
#######################################################################################################################################################################
@bot.message_handler(commands=['banlist'])
def banlist(m):
    text = m.text
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    bans = redis.smembers("banlist-{}".format(chatid))
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    banlist = "🚫لیست افراد محروم از گروه :\n\n"
    i = 0
    if chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True":
        for b in bans:
            i = i + 1
            banlist = str(banlist + i + " - " + b + "\n")
        bot.send_message(chatid , banlist)
#######################################################################################################################################################################
@bot.message_handler(commands=['link'])
def link(m):
    text = m.text
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    link = redis.smembers("link-{}".format(chatid))
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    if chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True":
        if link=="None":
            bot.send_message(chatid , "🥀شما هنوز لینک خود را ذخیره نکرده اید!")
        else:
            bot.send_message(chatid , "[{}]({})".format(m.chat.title , link) , disable_web_page_preview=True , parse_mode="Markdown")
#######################################################################################################################################################################
@bot.message_handler(commands=['ban'])
def ban(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    replied = m.reply_to_message
    replied_userid = m.reply_to_message.from_user.id
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    isbanned = str(redis.sismember("banlist-{}".format(chatid) , replied_userid))
    banisadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(replied_userid)))
    if chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True":
        if replied and isbanned=="False":
            if banisadmin=="True" or replied_userid in sudos:
                bot.send_message(chatid ,"⚜️من نمیتوانم مدیران گروه و مالکین خود را از گروه محروم کنم!")
            else:
                redis.sadd("banlist-{}".format(chatid) , replied_userid)
                bot.kick_chat_member(chatid , replied_userid)
                bot.send_message(chatid , "🚫کاربر مورد نظر با موفقیت به لیست محرومین افزوده شد!")
#######################################################################################################################################################################
@bot.message_handler(commands=['unban'])
def unban(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    replied = m.reply_to_message
    replied_userid = m.reply_to_message.from_user.id
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    isbanned = str(redis.sismember("banlist-{}".format(chatid) , replied_userid))
    banisadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(replied_userid)))
    if chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True":
        if replied and isbanned=="True":
            redis.srem("banlist-{}".format(chatid) , replied_userid)
            bot.send_message(chatid , "✨کاربر مورد نظر از لیست محرومین خارج گردید!")
        else:
            bot.send_message(chatid , "💫کاربر مورد نظر محدودیتی نداشت!")
#######################################################################################################################################################################
@bot.message_handler(commands=['settings'])
def locks(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    isadmin = str(redis.sismember("group-{}".format(chatid) , "{}".format(userid)))
    if chattype == "supergroup" and isadded=="True" and userid in sudos or isadmin=="True":
        bot.send_message(chatid , """🍃تنظیمات سوپرگروه به شرح زیر میباشد :
Lock text = {}""".format(lock_text(chatid , userid)))
#######################################################################################################################################################################

#######################################################################################################################################################################
try:
    bot.polling(True)
except:
    pass
