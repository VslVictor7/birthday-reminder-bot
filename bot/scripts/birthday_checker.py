from datetime import datetime
import os, asyncio
from dotenv import load_dotenv
from .birthday_database import has_sent_birthday_message, mark_birthday_sent

load_dotenv()

USER_ID = int(os.getenv("USER_ID"))
sent_birthdays = set()

def parse_birthdays(birthdays_str):
    birthdays = {}
    if birthdays_str:
        for item in birthdays_str.split(','):
            name, date = item.split(':')
            birthdays[name.strip()] = date.strip()
    return birthdays

async def send_birthday_messages(bot, birthdays, time_hours):
    today = datetime.now().strftime('%m-%d')
    birthday_friends = [name for name, date in birthdays.items() if date == today]

    if birthday_friends:
        print("[BIRTHDAYS] Lista de aniversariantes analisada.")
        user = bot.get_user(USER_ID)
        if user:
            for friend in birthday_friends:

                if not has_sent_birthday_message(friend):
                    await user.send(f"🎉 Hoje é o aniversário de {friend}! Dê parabéns a ele/ela! 🎂🎈")
                    print(f"[BIRTHDAYS] Mensagem de lembrete enviada para {user.name}.")
                    mark_birthday_sent(friend)
                print(f"[BIRTHDAYS] Mensagem de lembrete já foi enviada para {user.name}. Verificando novamente em 10 minutos.")
    else:
        print(f"[BIRTHDAYS] Lista de aniversariantes analisada, nenhum aniversário foi detectado hoje. Analisando novamente em {time_hours} horas.")

async def birthday_check_periodically(bot, birthdays, interval=18000):

    if not birthdays:
        print("[BIRTHDAYS] Nenhum aniversário listado. Saindo da função.")
        return

    while True:
        timer_hours = interval / 3600
        await send_birthday_messages(bot, birthdays, timer_hours)
        await asyncio.sleep(interval)