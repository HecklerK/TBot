import telebot
import constants
import time
import os
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://my-hit.fm')
time.sleep(15)
driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/span/span/span').click()
bot = telebot.TeleBot(constants.token)
#bot.send_message(292184500, "test")

#upd = bot.get_updates()

#last_upd = upd[-1]
#message_from_user = last_upd.message
#print(message_from_user)

print(bot.get_me())

def text(message):
    try:
        messag = message.text.lower()
        messag = re.sub("текст ", "", messag)
        messag = re.sub(" ", "+", messag)
        log(message, "Ищу текст песни " + messag)
        url = "http://www.pesni.net/search?q=" + messag
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="search_results"]/div[2]/div[1]/a').click()
        text = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/div/div/div[2]').text
        bot.send_message(message.chat.id, text)
    except:
        log(message, "текст песни " + messag + " не найден")
        bot.send_message(message.chat.id, "текст не найден")

def music(message):
    try:
        if message.text.startswith("Музыка") or message.text.startswith("музыка"):
            messag = message.text.lower()
            messag = re.sub("музыка ", "", messag)
            messag = re.sub(" ", "-", messag)
            url = "https://my-hit.fm/" + messag
        else:
            messag = re.sub(" ", "-", message.text)
            url = "https://my-hit.fm/" + messag
        log(message, "Ищу песню " + messag)
        driver.get(url)
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[3]/ul/li[1]/div[1]/ul/li[3]/a').send_keys(Keys.ENTER)
        time.sleep(3)
        im = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[3]/ul/li[1]/div[3]/h3/span[1]').text
        a = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[3]/ul/li[1]/div[3]/h3/span[2]').text
        ima = name(im, a)
        bot.send_message(message.chat.id, "минуточку")
        log(message, ima)
        n = 0
        while n <= 120:
            if os.path.exists("C:/Users/artem/Downloads/" + ima + ".mp3"):
                audio = open("C:/Users/artem/Downloads/" + ima + ".mp3", "rb")
                n = 121
            else:
                n += 1
                time.sleep(1)
        bot.send_message(message.chat.id, "песня найдена")
        bot.send_chat_action(message.from_user.id, "upload_audio")
        bot.send_audio(message.from_user.id, audio)
        log(message, "загружаю песню")
        audio.close()
        bot.send_message(message.chat.id, "Ссылка на музыку: " + url)
    except:
        x = 0
        while x < 1:
            bot.send_message(message.chat.id, "Песня не найдена попробуйте найти сами: " + url)
            log(message, "файл не найден")
            x = 1
        try:
            os.remove("C:/Users/artem/Downloads/" + ima + ".mp3")
        except:
            log(message, "файл не удалился")

#def translate(message):
    #messag = message.text.lower()
    #messag = re.sub("переведи ", "", messag)
    #log(message, "перевожу " + messag)
    #url = "https://translate.google.ru"
    #driver.get(url)

def name(im, a):
    ima = im + " - " + a
    #ima = re.sub(" ", "-", ima)
    #ima = re.sub(":", "-", ima)
    #ima = re.sub("\(", "", ima)
    #ima = re.sub("\)", "", ima)
    return ima

def vid(message):
    constants.cite = message.text


def log(message, answer):
    print("\n========")
    from datetime import  datetime
    print(datetime.now())
    print("сообщение от {0} {1}. (id = {2}) \n Текст - {3}".format(message.from_user.first_name,
                                                                 message.from_user.last_name,
                                                                 str(message.from_user.id),
                                                                 message.text))
    print(answer)

@bot.message_handler(commands= ['start'])
def hendle_text (message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row("/start", "/stop")
    user_markup.row("музыка")
    bot.send_message(message.from_user.id, "Привет", reply_markup = user_markup)

@bot.message_handler(commands= ['stop'])
def hendle_text (message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "..", reply_markup=hide_markup)

@bot.message_handler(commands= ['help'])
def hendle_text (message):
    bot.send_message(message.chat.id, "тест")

@bot.message_handler(content_types = ['text'])
def handle_text (message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.chat.id, "Привет")
        log(message, "Привет")
    elif message.text.startswith("Текст") or message.text.startswith("текст"):
        text(message)
    elif message.text == "Музыка" or message.text == "музыка" or message.text.startswith("Музыка") or message.text.startswith("музыка"):
        music(message)
    #elif message.text.startswith("Переведи") or message.text.startswith("переведи"):
       #translate(message)
    else:
        constants.name = message.text
        log(message, constants.name)
        bot.send_message(message.chat.id, "?")
        log(message, "?")
#try:
bot.polling(none_stop= True)
#except:
    #bot.send_message(292184500, "перезагружаюсь")
    #print("\nперезагружаюсь\n")
    #driver.quit()
    #os.system("Tbot.py")
    #exit()