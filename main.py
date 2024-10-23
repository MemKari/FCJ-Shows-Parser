import asyncio
import logging
import aiohttp

from bs4 import BeautifulSoup
from telethon import TelegramClient
from telethon.errors import PhoneNumberInvalidError, SessionPasswordNeededError

from config import api_id, api_hash, phone
from datadase.models import create_db_and_tables
from datadase.db_operations import are_posts_the_same, get_last_announcement_from_db

link = r'http://www.fcg.ge/rus/'


async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_last_header_from_website() -> str:
    html = await fetch_html(link)
    soup = BeautifulSoup(html, 'html.parser')
    last_post = soup.find('td', class_='contentheading')
    last_post_header = last_post.getText().strip()
    print(last_post_header)
    return last_post_header



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
    new_show_header = await get_last_header_from_website()
    await client.send_message(me.id, f'A New Dog Show in Georgia is announced! {new_show_header}, details here: {link}')



async def main():
    await create_db_and_tables()

    from_db = await get_last_announcement_from_db()
    from_website = await get_last_header_from_website()
    posts_the_same = await are_posts_the_same(from_db, from_website)

    if not posts_the_same:
        client = await create_tg_client()
        await send_tg_notification(client)


asyncio.run(main())

