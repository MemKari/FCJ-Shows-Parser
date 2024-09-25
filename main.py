import asyncio
from bs4 import BeautifulSoup
from requests import get
from telethon.sync import TelegramClient

from config import api_id, api_hash
from datadase.models import create_db_and_tables

link = r'http://www.fcg.ge/rus/'
response = get(link)
soup = BeautifulSoup(response.text, 'html.parser')


def get_last_announcement_text() -> str:
    #должен храниться в бд, здесь его из БД доставать
    last_announcement_header = '''CAC-CACIB FCI "RTVELI 2024" и "GEORGIAN WINNER 2024" -  Телави, Грузия'''
    return last_announcement_header

def get_new_show() -> bool:
    last_post = soup.find('td', class_='contentheading')
    last_post_header = last_post.getText().strip()

    print(last_post_header)

    last_announcement_text = get_last_announcement_text()
    if last_announcement_text != last_post_header:
        return True
    return False


def send_tg_notification():
    # отправить в телегу уведомление о новой выставке
    with TelegramClient("A New Dog's Show", api_id, api_hash) as client:
        me = client.get_me()
        client.send_message('me', '**bold** Уведомление о новой выставке собак!')


# print('заменить last_announcement_text на новый текст последней выставки в БД')

print(get_new_show())


async def main():
     await create_db_and_tables()


asyncio.run(main())

