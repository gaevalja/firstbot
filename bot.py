import discord
from discord.ext import commands
import datetime
import os


app = commands.Bot(command_prefix='/')
TOKEN = os.environ.get('BOT_TOKEN')


@app.event
async def on_ready():
    print('Done')
    await app.change_presence(status=discord.Status.online, activity=None)



@app.command()
async def startGettingMoney(ctx):
    await ctx.send("#주의#/startGettingMoney 명령어를 한번 더 사용하시면 total value가 초기화됩니다. 물론 김성주가 컴퓨터를 끄면 초기화되겠지용 ㅋ")
    total = 0
    n = 0
    dt = datetime.datetime.now()
    now_min = dt.minute
    while 1:
        if now_min != dt.minute:
            
            now_min = dt.minute
            total+=2.28310502283105
            n+=1
            await ctx.send("%d분동안 %lf원이 적립되었습니당 ㅋㅎㅋㅎ"%(n, total))    
        dt = datetime.datetime.now()
        

app.run(TOKEN)




