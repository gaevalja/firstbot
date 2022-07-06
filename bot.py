
import discord
from discord.ext import commands, tasks
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import string
import time
import header
from itertools import cycle
#heroku환경 여부
isOnHeroku = True
#if isOnHeroku:
TOKEN = os.environ.get('BOT_TOKEN')
# else:
date = int(time.strftime('%d', time.localtime(time.time())))

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

playing = cycle(['코', '딩', '몽', '키'])
#봇 등장 이벤트
@app.event
async def on_ready():
    print('Done')
    await app.change_presence(status=discord.Status.online, activity=None)
    await app.change_presence(activity=discord.Game(name="zzz"))
    checkday.start()
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

#header.init_workout_files()


@tasks.loop(seconds=3)
async def checkday():
    await app.change_presence(activity=discord.Game(next(playing)))
    if header.checkday(date):
        for workout in header.workout_list.keys():
            with open('textfile/'+workout+'_tmp.txt', 'w', encoding = 'utf-8') as file:
                file.write('0')
    return

@app.command()  
async def 운동(ctx, workout, workout_cnt=None):
    if workout == 'check':
        workoutlist = list()
        cntlist = list()
        for workout_ in header.workout_list:
            with open('textfile/'+workout_+'_tmp.txt', 'r', encoding = 'utf-8') as file:
                workoutlist.append(workout_)
                cntlist.append(header.workout_list[workout_]-int(file.read()))
        workoutlist_total = list()
        cntlist_total = list()
        for workout_ in header.workout_list:
            with open('textfile/'+workout_+'_total.txt', 'r', encoding = 'utf-8') as file:
                workoutlist_total.append(workout_)
                cntlist_total.append(int(file.read()))
                
        await ctx.channel.send('-----------TODAY-----------')
        cnt = 0
        for i, j in zip(workoutlist, cntlist):
            if j<=0:
                cnt += 1
                continue
            await ctx.channel.send('%s은 %d개 더 하셔야 합니다.'%(i, j))
        if cnt == 3:
            await ctx.channel.send('오.운.완')
        
        await ctx.channel.send('-----------TOTAL-----------')
        for i, j in zip(workoutlist_total, cntlist_total):
            await ctx.channel.send('%s은 총 %d개 하셨습니다.'%(i, j))
        return
    if workout == 'list':
        await ctx.channel.send('운동종류:목표개수 -> '+str(header.workout_list))
        return
    additional_message = ''
    if workout not in header.workout_list:
        await ctx.channel.send("운동이 등록되지 않았습니다. 운동 종류와 개수 등록을 원하시면 관리자 김성주에게 요청 하던가 말던가 해보셩 ㅋ")
    elif int(workout_cnt) <= 0:
        await ctx.channel.send("양수를 입력하세요 애야 ㅋ")
    else:
        with open('textfile/'+workout+'_tmp.txt', 'r', encoding = 'utf-8') as file:
            tmp_cnt = int(file.read())
            if tmp_cnt + int(workout_cnt) >= header.workout_list[workout]:
                additional_message = ' 하루 목표치 '+str(header.workout_list[workout])+'개 를 달성하였습니다.'
        with open('textfile/'+workout+'_tmp.txt', 'w', encoding = 'utf-8') as file:
            file.write(str(tmp_cnt+int(workout_cnt)))
        with open('textfile/'+workout+'_total.txt', 'r', encoding = 'utf-8') as file:
            total_cnt = int(file.read())
        with open('textfile/'+workout+'_total.txt', 'w', encoding = 'utf-8') as file:
            total_cnt += int(workout_cnt)
            file.write(str(total_cnt))
        await ctx.channel.send('오늘 '+workout+' 을 '+str(tmp_cnt+int(workout_cnt))+'개 했습니다.'+additional_message)

    
        
#####            
app.run(TOKEN)
#####
