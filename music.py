from ast import Await
import discord
from discord import client
from discord.ext import commands
from youtube_dl import YoutubeDL
import time
import asyncio
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import os
from urllib import request
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

user = [] #유저가 입력한 입악정보
musictitle = [] #가공된 노래제목
song_queue = [] #가공된 노래링크
musicnow = [] #현재 출력되는 노래 배열

shuffles = []


userF = []
userFlist = []
allplaylist = []

number = 1

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = R"C:\Users\Somma\Downloads\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options = options)
    driver.get("https://www.youtube.com/results?search_query="+msg)
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    
    return music, URL

def play(ctx):
    global Vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    Vc = get(bot.voice_clients, guild=ctx.guild)
    if not Vc.is_playing():
        Vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not Vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            Vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

    else:
        if not Vc.is_playing():
            client.loop.create_task(Vc.disconnect())


def again(ctx, url):
    global number
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if number:
        with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        if not Vc.is_playing():
            Vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: again(ctx, url))

def load_chrome_driver():
      
    options = webdriver.ChromeOptions()

    options.binary_location = os.getenv('GOOGLE_CHROME_BIN')

    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    return webdriver.Chrome(executable_path=str(os.environ.get('CHROME_EXECUTABLE_PATH')), chrome_options=options)


@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(".p"))

@bot.command()
async def 들어와(ctx):
    try:
        global Vc
        Vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await Vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("아무도 없어서 제가 못가요. ")

@bot.command()
async def 나가(ctx):
    try:
        await Vc.disconnect()
    except:
        await ctx.send("다떼가 일을 안해서 제가 없어요.")


@bot.command()
async def 명령어(ctx):
    await ctx.send(embed = discord.Embed(title='도움말',description="""
\.명령어 -> 뮤직봇의 모든 명령어를 볼 수 있습니다.

\.p [제목 or 링크] -> 클랜봇이 노래를 검색해 틀어줍니다.

\.지금노래 -> 지금 재생되고 있는 노래의 제목을 알려줍니다.

\.반복재생 [제목 or 링크] -> 지금 재생되고 있는 노래를 반복재생 해줍니다.

\.멜론차트 -> 최신 멜론차트를 재생합니다.

\.목록 -> 이어서 재생할 노래목록을 보여줍니다.

\.재생 -> 목록에 추가된 노래를 재생합니다.

\.초기화 -> 목록에 추가된 모든 노래를 지웁니다.

\.추가 [노래] -> 노래를 대기열에 추가합니다.

\.삭제 [숫자] -> 대기열에서 입력한 숫자에 해당하는 노래를 지웁니다.

\.셔플 -> 대기열을 랜덤으로 섞어줍니다.

\.티키틱 -> 티키틱 노래 모음을 들려드립니다.

\.투표 [글] -> 해당 글과 관련된 투표란을 만들어줍니다.

\.문제 [글] -> 해당 글과 관련된 문제를 만들어줍니다.   """, color = 0x00ff00))

@bot.command()
async def 엘프고(ctx):
    await ctx.send(embed = discord.Embed(title='ʚ엘프고ɞ 추천글',description="""
1. https://cafe.naver.com/onimobile/11997053 (비정상 팟)

2. https://cafe.naver.com/onimobile/11993472 (챕터1 스피드런 공략)

3. https://cafe.naver.com/onimobile/12007157 (챕터2 스피드런 공략) """, color = 0x00ff00))

@bot.command()
async def URL(ctx, *, url):
    try:
        global Vc
        Vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await Vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("아무도 없어요. ")

    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not Vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        Vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + url + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")   
    embed = discord.Embed(color = 0x00ff00)
    embed.add_field(name = "⏯ 일시정지  ⏹ 노래끄기", value = "⏸ 다시재생  📋 목록", inline = False)
    Flist = await ctx.send(embed = embed)
    await Flist.add_reaction("⏯")
    await Flist.add_reaction("⏸")
    await Flist.add_reaction("⏹")
    await Flist.add_reaction("📋")

@bot.command()
async def p(ctx, *, msg):

    try:
        global Vc
        Vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await Vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("아무도 없어요. ")

    if not Vc.is_playing():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = R"C:\Users\Somma\Downloads\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query="+msg)
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+ musicurl

        driver.quit()

        musicnow.insert(0, entireText)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        Vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    else:
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send("지금" + result + "노래가 재생중이라 대기열로 이동했어요.")
    embed = discord.Embed(color = 0x00ff00)
    embed.add_field(name = "⏯ 일시정지  ⏹ 노래끄기", value = "⏸ 다시재생  📋 목록", inline = False)
    Flist = await ctx.send(embed = embed)
    await Flist.add_reaction("⏯")
    await Flist.add_reaction("⏸")
    await Flist.add_reaction("⏹")
    await Flist.add_reaction("📋")


@bot.command()
async def 티키틱(ctx):

    try:
        global Vc
        Vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await Vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("아무도 없어요. ")

    if not Vc.is_playing():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = R"C:\Users\Somma\Downloads\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query="+"티키틱 노래모음"+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        musicnow.insert(0, entireText)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        Vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    embed = discord.Embed(color = 0x00ff00)
    embed.add_field(name = "⏯ 일시정지  ⏹ 노래끄기", value = "⏸ 다시재생  📋 목록", inline = False)
    Flist = await ctx.send(embed = embed)
    await Flist.add_reaction("⏯")
    await Flist.add_reaction("⏸")
    await Flist.add_reaction("⏹")
    await Flist.add_reaction("📋")

@bot.command()
async def 멜론차트(ctx):

    try:
        global Vc
        Vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await Vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("아무도 없어요. ")

    if not Vc.is_playing():
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = R"C:\Users\Somma\Downloads\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query=멜론차트")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        Vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")
    embed = discord.Embed(color = 0x00ff00)
    embed.add_field(name = "⏯ 일시정지  ⏹ 노래끄기", value = "⏸ 다시재생  📋 목록", inline = False)
    Flist = await ctx.send(embed = embed)
    await Flist.add_reaction("⏯")
    await Flist.add_reaction("⏸")
    await Flist.add_reaction("⏹")
    await Flist.add_reaction("📋")


@bot.command()
async def 일시정지(ctx):
    if Vc.is_playing():
        Vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = musicnow[0] + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()
async def 다시재생(ctx):
    try:
        Vc.resume()
    except:
         await ctx.send("지금 노래가 재생되지 않네요.")
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = musicnow[0]  + "을(를) 다시 재생했습니다.", color = 0x00ff00))

@bot.command()
async def 노래끄기(ctx):
    if Vc.is_playing():
        Vc.stop()
        global number
        number = 0
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = musicnow[0]  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()
async def 반복재생(ctx, *, msg):
      
    try:
        global Vc
        Vc = await ctx.message.author.voice.channel.connect()   
    except:
        try:
            await Vc.move_to(ctx.message.author.voice.channel)
        except:
            pass

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    
    global entireText
    global number
    number = 1
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(musicnow) - len(user) >= 1:
        for i in range(len(musicnow) - len(user)):
            del musicnow[0]

    chromedriver_dir = R"C:\Users\Somma\Downloads\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options = options)
    driver.get("https://www.youtube.com/results?search_query="+msg)
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    entireText = entireNum.text.strip()
    musicnow.insert(0, entireText)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    await ctx.send(embed = discord.Embed(title= "반복재생", description = "현재 " + musicnow[0] + "을(를) 반복재생하고 있습니다.", color = 0x00ff00))
    again(ctx, url)
    embed = discord.Embed(color = 0x00ff00)
    embed.add_field(name = "⏯ 일시정지  ⏹ 노래끄기", value = "⏸ 다시재생  📋 목록", inline = False)
    Flist = await ctx.send(embed = embed)
    await Flist.add_reaction("⏯")
    await Flist.add_reaction("⏸")
    await Flist.add_reaction("⏹")
    await Flist.add_reaction("📋")

@bot.command()
async def 지금노래(ctx):
    global Ftext
    correct = 0
    global Flist
    if not Vc.is_playing():
        await ctx.send("지금은 노래가 재생되지 않네요..")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))

@bot.command()
async def 추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 추가했어요!")

@bot.command()
async def 삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없어 삭제할 수 없어요!")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났습니다!")
            else:
                await ctx.send("숫자를 입력해주세요!")

@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))

@bot.command()
async def 초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """목록이 정상적으로 초기화되었습니다.""", color = 0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")

@bot.command()
async def 재생(ctx):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(user) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")

    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not Vc.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생되고 있어요!")

@bot.command()
async def 스킵(ctx):
    if len(user) > 1:
        if Vc.is_playing():
            Vc.stop()
            global number
            number = 0
            await ctx.send(embed = discord.Embed(title = "스킵", description = musicnow[1] + "을(를) 다음에 재생합니다!", color = 0x00ff00))
        else:
            await ctx.send("노래가 이미 재생되고 있어요!")
    else:
        await ctx.send("목록에 노래가 2개 이상 없네요..")

@bot.command()
async def 셔플(ctx):
    try:                                                                                                                                                                                                                                                     
        global musicnow, user, musictitle,song_queue
        numbershuffle = len(musicnow) - len(user)
        for i in range(numbershuffle):
            shuffles.append(musicnow[0])
            del musicnow[0]
        combine = list(zip(user, musicnow, musictitle, song_queue))
        random.shuffle(combine)
        a, b, c, d = list(zip(*combine))

        user = list(a)
        musicnow = list(b)
        musictitle = list(c)
        song_queue = list(d)

        for i in range(numbershuffle):
            musicnow.insert(0, shuffles[i])

        del shuffles[:]
        await ctx.send("목록이 정상적으로 셔플되었습니다.")
    except:
        await ctx.send("셔플할 목록이 없습니다!")

@bot.command()
async def 투표(ctx, *, number):
    global Ftext
    correct = 0
    global Flist
    titlename = str(ctx.message.author.name) + "님의 투표"
    embed = discord.Embed(title = titlename, description = number, color = 0x00ff00)
    embed.add_field(name = "맞다:o:", value = "⠀", inline = False)
    embed.add_field(name = "아니다:x:", value = "⠀", inline = False)
    Flist = await ctx.send(embed = embed)
    await Flist.add_reaction("⭕")
    await Flist.add_reaction("❌")

@bot.command()
async def 문제(ctx, *, number):
    global Ftext
    correct = 0
    global Flist
    titlename = str(ctx.message.author.name) + "님의 문제"
    embed = discord.Embed(title = titlename, description = number, color = 0x00ff00)
    embed.add_field(name = "매우 그렇다/그렇다/보통이다/아니다/매우 아니다", value = "⠀", inline = False)
    Flist = await ctx.send(embed = embed)
    await Flist.add_reaction("1️⃣")
    await Flist.add_reaction("2️⃣")
    await Flist.add_reaction("3️⃣")
    await Flist.add_reaction("4️⃣")
    await Flist.add_reaction("5️⃣")


@bot.command()
async def 리모컨(ctx):
    global Ftext
    correct = 0
    global Flist
    titlename = str(ctx.message.author.name) + "님의 노래 리모컨"
    if not Vc.is_playing():
        await ctx.send("지금은 노래가 재생되지 않네요..")
    embed = discord.Embed(color = 0x00ff00)
    embed.add_field(name = "⏯ 일시정지  ⏹ 노래끄기", value = "⏸ 다시재생  📋 목록", inline = False)
    Flist = await ctx.send(embed = embed)
    await Flist.add_reaction("⏯")
    await Flist.add_reaction("⏸")
    await Flist.add_reaction("⏹")
    await Flist.add_reaction("📋")

@bot.event
async def on_reaction_add(reaction, users):
    if users.bot == 1:
        pass
    else:
            if str(reaction.emoji) == '⏯':
                if Vc.is_playing():
                    Vc.pause()
                    
            elif str(reaction.emoji) == '⏹':
                if Vc.is_playing():
                   Vc.stop()
                   global number
                   number = 0
                   

            
            
            elif str(reaction.emoji) == '⏸':
                    Vc.resume()
               
                

            elif str(reaction.emoji) == '📋':
                global Text
                Text = ""
                for i in range(len(musictitle)):
                   Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
                   await reaction.message.channel.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))


access_token = os.environ["BOT_TIKEN"]
bot.run(access_token)
