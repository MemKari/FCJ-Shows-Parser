from bs4 import BeautifulSoup
from requests import get


link = r'http://www.fcg.ge/rus/'
response = get(link)
soup = BeautifulSoup(response.text, 'html.parser')

last_post = soup.find('td', class_='contentheading')
result = last_post.getText().strip()

last_announcement = '''CAC-CACIB FCI "RTVELI 2024" и "GEORGIAN WINNER 2024" -  Телави, Грузия'''

if last_announcement != result:
    print("отправить в телегу уведомление о новой выставке")
    print('заменить last_announcement на новый текст последней выставки в БД')
    print(soup.title)
    print(result)