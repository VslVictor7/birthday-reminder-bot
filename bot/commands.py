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
        # Verifica se está em um canal de mensagem direta (DM)
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.defer(ephemeral=True)  # Defere a resposta (indica que vai demorar um pouco)

            count = 0
            async for message in interaction.channel.history(limit=100):
                if message.author == bot.user:
                    await message.delete()
                    count += 1

            # Envia a resposta final
            await interaction.followup.send(f"{count} mensagens apagadas.")
        else:
            # Resposta caso o comando não esteja em uma DM
            await interaction.response.send_message(
                "Este comando só funciona em mensagens diretas (DMs).",
                ephemeral=True,
            )