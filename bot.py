
import discord
from discord.ext import commands
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import string
import time


#heroku환경 여부
isOnHeroku = True
#if isOnHeroku:
TOKEN = os.environ.get('BOT_TOKEN')
# else:


#옵션 설정
options = webdriver.ChromeOptions()
if isOnHeroku:
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("disable-dev-shm-usage")
options.add_argument('window-size=1920x1080')
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

options.add_argument("--lang=ko_KR")
options.add_argument("--lang=ko")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#caps = DesiredCapabilities().CHROME
#caps["pageLoadStrategy"] = "none"

#명령접두사
app = commands.Bot(command_prefix='/')

#봇 등장 이벤트
@app.event
async def on_ready():
    print('Done')
    await app.change_presence(status=discord.Status.online, activity=None)


badwords = ['ㅅㅂ', 'tq', '시발', '개객', 'ㅈㄴ', '개**', 'ㅆㅂ', 'Tq', 'lqkf', '개라석', '애가', 'ㅄ', 'ㅂㅅ', '병신', '븅신', '존나', '슈발']
@app.event
async def on_message(message):
   for i in badwords: # Go through the list of bad words;
        if i in message.content:
            await message.delete()
            await message.channel.send(f"{message.author.mention} 나쁜말감지")
            app.dispatch('profanity', message, i)
            return # So that it doesn't try to delete the message again, which will cause an error.
        await app.process_commands(message)

#명령어
@app.command()
async def hello(ctx):
    await ctx.send("me too")
    


@app.command()
async def find(ctx, user_input):
    #
    if isOnHeroku:
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    else:
        driver = webdriver.Chrome(executable_path='C:/JUNGz_KOR/chromedriver.exe', options=options)
    driver.implicitly_wait(5)
    if user_input.isalpha(): #영어 입력시 주소
        URL = 'https://en.dict.naver.com/#/search?query='+user_input+'&range=all'
    else:#한글 입력시 주소
        URL = 'https://ko.dict.naver.com/#/search?query='+user_input+'&range=all'
    driver.get(URL)
    
    #버튼 누르고 새로운 주소 들어가기
    #input_box = driver.find_element_by_css_selector('#ac_input')
    #input_box.send_keys(user_input)
    #input_box.send_keys(Keys.ENTER)
    #
    try:
        word = driver.find_element_by_css_selector('#searchPage_entry > div > div:nth-child(1) > ul > li:nth-child(1) > p').text
        await ctx.send(word)
    except:
        await ctx.send("응 ㅇㄴㅇ")
    driver.quit()   
    #
    
@app.command()
async def pubg(ctx, user_input):
    if isOnHeroku:
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    else:
        driver = webdriver.Chrome(executable_path='C:/JUNGz_KOR/chromedriver.exe', options=options)
    driver.implicitly_wait(5)
    URL = 'https://dak.gg/pubg/?hl=ko-KR'
    driver.get(URL)
    #user 페이지 접속
    input_box = driver.find_element_by_css_selector('#__layout > div > main > section.Search.d-none.d-sm-block > div > form > input')
    input_box.send_keys(user_input)
    input_box.send_keys(Keys.ENTER)
    
    #k/d
    try:
        squad_kd = driver.find_element_by_css_selector('#__layout > div > main > div:nth-child(4) > div > section.Overview > section.Overview__normals > div > section:nth-child(3) > dl > div:nth-child(1) > dd.Stat__value.Stat__value--kda').text
        print(type(squad_kd))
        await ctx.send('K/D: %s'%format(squad_kd))
        if float(squad_kd)<1.00:
            await ctx.send('사람인가 ㅋㅋ :nauseated_face: ')
        elif float(squad_kd)<2.00:
            await ctx.send('에효 ㅋㅋ :face_vomiting: ')
        else:
            await ctx.send('좀치네')
        driver.quit()
    except:
        await ctx.send('error')
        driver.quit()


@app.command()  
async def 피파수수료계산(ctx,cash,topclass,pc):
    cash=int(cash)
    if cash<1000000000:
        await ctx.channel.send("~~~~~구단가치 계산중 ~~~")
        time.sleep(4)
        await ctx.channel.send("ㄺㅎㅃ 그것도 구단이냐 ㅋ")
        
    elif topclass=="참":
        if pc=="참":
            cashreturn= "{:,}".format(cash-(cash*(0.4))+((cash*(0.4))*0.5))
            await ctx.channel.send("수령 예상 금액은 약 %s BP 입니다." %cashreturn)

        else:
            cashreturn= "{:,}".format(cash-(cash*(0.4))+((cash*(0.4))*0.2))
            await ctx.channel.send("수령 예상 금액은 약 %s BP 입니다." %cashreturn)

    else:
        if pc=="참":
            cashreturn= "{:,}".format(cash-(cash*(0.4))+((cash*(0.4))*0.3))
            await ctx.channel.send("수령 예상 금액은 약 %s BP 입니다." %cashreturn)

        else:
            cashreturn= "{:,}".format((cash*0.6))
            await ctx.channel.send("수령 예상 금액은 약 %s BP 입니다." %cashreturn)
            
#####            
app.run(TOKEN)
#####