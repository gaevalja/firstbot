import discord
from discord.ext import commands
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#


app = commands.Bot(command_prefix='plz')
TOKEN = os.environ.get('BOT_TOKEN')


@app.event
async def on_ready():
    print('Done')
    await app.change_presence(status=discord.Status.online, activity=None)



@app.command()
async def find(ctx, user_input):
    #
    driver = webdriver.Chrome('chromedriver.exe',options=options)
    driver.implicitly_wait(3)
    driver.get('https://ko.dict.naver.com/#/main' )
    #
    input_box = driver.find_element_by_css_selector('#ac_input')
    input_box.send_keys(user_input)
    input_box.send_keys(Keys.ENTER)
    #
    word = driver.find_element_by_css_selector('#searchPage_entry > div > div:nth-child(1) > ul > li:nth-child(1) > p').text
    print(word)
    driver.quit()   
    #
    await ctx.send("'",word+"'"+' 라는 뜻 ㅋ')
app.run(TOKEN)

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# #
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# #
# driver = webdriver.Chrome('chromedriver.exe',options=options)
# driver.implicitly_wait(3)
# driver.get('https://ko.dict.naver.com/#/main' )

# input_box = driver.find_element_by_css_selector('#ac_input')
# input_box.send_keys('애미')
# input_box.send_keys(Keys.ENTER)

# word = driver.find_element_by_css_selector('#searchPage_entry > div > div:nth-child(1) > ul > li:nth-child(1) > p').text
# print(word)
# driver.quit()



