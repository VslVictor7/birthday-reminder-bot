import discord
import os
from scripts.mybot import MyBot
from scripts.birthday_database import create_birthday_data
from scripts.birthday_checker import parse_birthdays, birthday_check_periodically
from commands import setup_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
FRIENDS_BIRTHDAYS = os.getenv('BIRTHDAYS')

# Rodar o bot.

bot = MyBot()

@bot.event
async def on_ready():

    print(f"[BOT] Logado como {bot.user.name} - {bot.user.id}")

    activity = discord.Activity(type=discord.ActivityType.watching, name="Quem são os aniveriantes!")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    await background_tasks()

    create_birthday_data()

    try:
        parsed_birthdays = parse_birthdays(FRIENDS_BIRTHDAYS)
        print("[BOT STARTED] Pronto para monitoramento de Aniversariantes.")

        await birthday_check_periodically(bot, parsed_birthdays)

    except discord.DiscordException as e:
        print(f"[BOT ERROR] Erro ao buscar aniversários: {e}")
        await bot.close()


async def background_tasks():
    await bot.wait_until_ready()

    bot.loop.create_task(setup_commands(bot))
    bot.loop.create_task(bot.sync_commands())

bot.run(TOKEN)