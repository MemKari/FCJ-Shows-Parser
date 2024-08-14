from bs4 import BeautifulSoup
from requests import get


link = r'http://www.fcg.ge/rus/'
response = get(link)
soup = BeautifulSoup(response.text, 'html.parser')

last_post = soup.find('td', class_='contentheading')
last_post_text = last_post.getText().strip()

last_announcement_text = '''CAC-CACIB FCI "RTVELI 2024" и "GEORGIAN WINNER 2024" -  Телави, Грузия'''

if last_announcement_text != last_post_text:
    print("отправить в телегу уведомление о новой выставке")
    print('заменить last_announcement_text на новый текст последней выставки в БД')
    print(soup.title)
    print(last_post_text)