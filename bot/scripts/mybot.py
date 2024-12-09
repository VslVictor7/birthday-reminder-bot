import discord
import os
import pytz
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

IP = os.getenv('MINECRAFT_SERVER')

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def sync_commands(self):
        try:
            await self.tree.sync()
            print("[BOT SYNC] Comandos sincronizados globalmente.")

        except Exception as e:
            print(f"[BOT ERROR] Falha ao sincronizar os comandos: {e}")
        except discord.errors.HTTPException as e:
            if e.code == 429:
                retry_after = e.retry_after
                print(f"[BOT ERROR] Rate limitado. Tentando novamente em  {retry_after} segundos.")
                await asyncio.sleep(retry_after)
            else:
                print(f"[BOT ERROR] Falha ao sincronizar os comandos: {e}")