import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from scoutf import do_ocr
from tranquilizer import setPrompt
from slime import getAnswer

load_dotenv()
disc_Token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='--',intents=intents)

@bot.event
async def on_ready():
    print(f'Bot online')

@bot.command()
async def verify(ctx):
    if ctx.author == bot.user:
        return
    if not ctx.message.attachments:
        ctx.reply("Você precisa enviar uma foto para usar esse comando")

    img_url = ctx.message.attachments[0].url
    answer = do_ocr(img_url)
    teacher_mode = setPrompt(answer)
    response = getAnswer(teacher_mode)

    MAX_LENGTH = 2000
    for i in range(0, len(response), MAX_LENGTH):
        await ctx.send(response[i:i+MAX_LENGTH])



bot.run(disc_Token)