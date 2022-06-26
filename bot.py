import discord
from discord.ext import commands
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#
options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument('window-size=1920x1080')
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#


app = commands.Bot(command_prefix='/')
TOKEN = os.environ.get('BOT_TOKEN')


@app.event
async def on_ready():
    print('Done')
    await app.change_presence(status=discord.Status.online, activity=None)

@app.command()
async def hello(ctx):
    await ctx.send("me too")

@app.command()
async def find(ctx, user_input):
    await ctx.send("1")####
    #
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    await ctx.send("2")####
    driver.implicitly_wait(5)
    driver.get('https://ko.dict.naver.com/#/main' )
    #
    input_box = driver.find_element_by_css_selector('#ac_input')
    input_box.send_keys(user_input)
    input_box.send_keys(Keys.ENTER)
    #
    try:
        word = driver.find_element_by_css_selector('#searchPage_entry > div > div:nth-child(1) > ul > li:nth-child(1) > p').text
        await ctx.send(word)
    except:
        await ctx.send("응 ㅇㄴㅇ")
    driver.quit()   
    #
    

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
# input_box.send_keys('나무')
# input_box.send_keys(Keys.ENTER)

# word = driver.find_element_by_css_selector('#searchPage_entry > div > div:nth-child(1) > ul > li:nth-child(1) > p').text
# print(word)
# driver.quit()



