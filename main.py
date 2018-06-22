# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
KingAPI
Version 1.0
Code by PrinceDell
KingCompany
"""

#//=====----- Libraries -----=====\\#
import os
import sys
import urllib
import time
import telebot
import termcolor
import platform
import redis as Redis
from termcolor import colored
from telebot import types,util
from time import sleep
#//=====----- Config-1 -----=====\\#
reload(sys)
sys.setdefaultencoding("utf-8")
redis = Redis.StrictRedis(host="localhost" , port=6379)
#===================================#
token = "601270288:AAHfClZ7pKBLno4lI01fNQYOCfNWBElbhvQ"
bot = telebot.TeleBot(token)
sudo_users = [ 478026278,1,2,3,4 ]
channel_username = "WINEY"
#===================================#
channel = types.InlineKeyboardMarkup()
channel.add(types.InlineKeyboardButton(text="C H A N N E L" , url="t.me/{}".format(channel_username)))
#===================================##===================================#
def muteall(m):
    if str(redis.sismember("muteall" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def lockphoto(m):
    if str(redis.sismember("photo" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def lockvideo(m):
    if str(redis.sismember("video" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def lockvoice(m):
    if str(redis.sismember("voice" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def locktext(m):
    if str(redis.sismember("text" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def lockgif(m):
    if str(redis.sismember("gif" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def locksticker(m):
    if str(redis.sismember("sticker" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def lockmusic(m):
    if str(redis.sismember("music" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def locklocation(m):
    if str(redis.sismember("location" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def lockcontact(m):
    if str(redis.sismember("contact" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def locklink(m):
    if str(redis.sismember("link" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
def lockgame(m):
    if str(redis.sismember("game" , m))=="True":
        return "LOCKED"
    else:
        return "UNLOCKED"
#===================================##===================================#
@bot.message_handler(commands=['add'])
def add(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    ismod = bot.get_chat_member(chatid , userid).status
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    if chattype == "supergroup" and isadded=="False" and userid in sudo_users or ismod!="member":
        redis.sadd("groups" , "{}".format(chatid))
        bot.send_message(chatid , "*⌥ Supergroup [ {} ] has been added to database by [ {} ]!*".format(m.chat.title , userid) , "Markdown" , channel)
    elif chattype == "supergroup" and isadded=="True" and userid in sudos:
        bot.send_message(chatid , "*⌥ Supergroup [ {} ] is alreay in database!*".format(m.chat.title) , "Markdown" , channel)
#######################################################################################################################################################################
@bot.message_handler(commands=['rem'])
def rem(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    ismod = bot.get_chat_member(chatid , userid).status
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    if chattype == "supergroup" and isadded=="False" and userid in sudos or ismod!="member":
        redis.srem("groups" , "{}".format(chatid))
        bot.send_message(chatid , "*- Supergroup [ {} ] has been removed from database by [ {} ]*".format(m.chat.title , userid) , "Markdown" , channel)
    elif chattype == "supergroup" and isadded=="False" and userid in sudos:
        bot.send_message(chatid , "*- Supergroup [ {} ] is not on of my group!*".format(m.chat.title) , "Markdown" , channel)
#===================================##===================================#
@bot.message_handler(commands=['settings'])
def locks(m):
    userid = m.from_user.id
    chatid = m.chat.id
    chattype = m.chat.type
    ismod = bot.get_chat_member(chatid , userid).status
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    if chattype == "supergroup" and isadded=="True" and userid in sudos or ismod!="member":
        bot.send_message(chatid , """*MuteAll* : _[{}]_
*Photo* : _[LOCKED]_
*Video* : _[LOCKED]_
*Voice* : _[LOCKED]_
*Sticker* : _[LOCKED]_
*Text* : _[LOCKED]_""".format(muteall(chatid)) , "Markdown" , channel)
#===================================##===================================#
@bot.message_handler(commands=['ping'])
def ping(m):
    if m.chat.type=="supergroup":
        bot.send_message(m.chat.id , "*⌥ ONLINE AT ALL THE TIME!*" , "Markdown")
#===================================##===================================#
#===================================##===================================##===================================##===================================#
@bot.message_handler(commands=['lock'])
def locks(m):
    chatid = m.chat.id
    userid = m.from_user.id
    ismod = bot.get_chat_member(chatid , userid).status
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    lock = m.text.split()[1]
    if isadded=="True" and m.chat.type=="supergroup":
        if lock=="photo" and (ismod!="member" or userid in sudo_users):
            if lockphoto(chatid)!="LOCKED":
                redis.sadd("photo" , chatid)
                bot.send_message(chatid , "*⌥ Lock {} has been enabled!*".format(lock) , "Markdown")
            else:
                bot.send_message(chatid , "*⌥ Lock {} is alreay locked here.*".format(lock) , "Markdown")
        if lock=="text" and (ismod!="member" or userid in sudo_users):
            if locktext(chatid)!="LOCKED":
                redis.sadd("text" , chatid)
                bot.send_message(chatid , "*⌥ Lock {} has been enabled!*".format(lock) , "Markdown")
            else:
                bot.send_message(chatid , "*⌥ Lock {} is alreay locked here.*".format(lock) , "Markdown")
#===================================##===================================#

#===================================##===================================#
@bot.message_handler(content_types=['photo'])
def locks_deleting(m):
    chatid = m.chat.id
    userid = m.from_user.id
    ismod = bot.get_chat_member(chatid , userid).status
    isadded = str(redis.sismember("groups" , "{}".format(chatid)))
    lock = m.text.split()[1]
    if m.chat.type=="supergroup" and isadded=="True" and lockphoto=="LOCKED":
        if ismod=="member" or userid not in sudo_users:
            bot.delete_message(chatid , m.message_id)
#===================================##===================================#
while True:
    try:
        bot.polling(True)
    except:
        continue
