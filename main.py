import asyncio
import logging
import aiohttp

from bs4 import BeautifulSoup
from telethon import TelegramClient
from telethon.errors import PhoneNumberInvalidError, SessionPasswordNeededError

from config import api_id, api_hash, phone
from datadase.models import create_db_and_tables

link = r'http://www.fcg.ge/rus/'


async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_new_show():
    html = await fetch_html(link)
    soup = BeautifulSoup(html, 'html.parser')
    last_post = soup.find('td', class_='contentheading')
    last_post_header = last_post.getText().strip()
    print(last_post_header)
    return True


async def create_tg_client():
    client = TelegramClient('session_name', api_id, api_hash)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code = input('Enter the code you received: ')
            await client.sign_in(phone, code)
    except PhoneNumberInvalidError:
        logging.info('Invalid phone number.')
    except SessionPasswordNeededError:
        password = input('Enter your 2FA password: ')
        await client.sign_in(password=password)

    me = await client.get_me()
    logging.info(f'Telegram: Logged in as {me.first_name} {me.last_name} ({me.username})')
    logging.info("Telegram: Event handlers added")
    return client


async def send_tg_notification(client):
    me = await client.get_me()
    await client.send_message(me.id, 'Привет! Это сообщение самому себе.')


async def main():
    await create_db_and_tables()
    client = await create_tg_client()
    await send_tg_notification(client)
    await get_new_show()


asyncio.run(main())

