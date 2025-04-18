import discord
import pytz
from datetime import datetime

def create_embed(title, description, color):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    embed.timestamp = datetime.now(pytz.timezone("America/Sao_Paulo"))
    return embed

async def setup_commands(bot):

    @bot.tree.command(name="limpar_dms", description="Apaga mensagens do bot na DM atual.")
    async def limpar_dms(interaction: discord.Interaction):

        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.defer(ephemeral=True)

            count = 0
            async for message in interaction.channel.history(limit=100):
                if message.author == bot.user:
                    await message.delete()
                    count += 1

            await interaction.followup.send(f"{count} mensagens apagadas.")
        else:
            await interaction.response.send_message(
                "Este comando só funciona em mensagens diretas (DMs).",
                ephemeral=True,
            )