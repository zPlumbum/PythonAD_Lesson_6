from pprint import pprint
import requests
from bs4 import BeautifulSoup
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/all/'


# Задание №1
def scrap_habr_posts(pages_count):
    posts_list = []

    for page in range(1, pages_count + 1):
        page_url = f'{URL}page{page}/'
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for post in soup.find_all('article', class_='post'):
            hub_tags = post.find_all('a', class_='hub-link')
            hub_tags = list(map(lambda x: x.text, hub_tags))

            for tag in hub_tags:
                if tag.lower() in KEYWORDS:
                    title = post.find('a', class_='post__title_link').text
                    href = post.find('a', class_='post__title_link')['href']
                    posts_list.append({'date': f'{datetime.now()}', 'title': title, 'url': href})
                    break

    return posts_list


# Задание №2
def scrap_habr_posts_v2(pages_count):
    posts_list = []

    for page in range(1, pages_count + 1):
        page_url = f'{URL}page{page}/'
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for post in soup.find_all('article', class_='post'):
            hub_tags = post.find_all('a', class_='hub-link')
            hub_tags = list(map(lambda x: x.text, hub_tags))
            post_url = post.find('a', class_='post__title_link')['href']

            tag_exists = False
            for tag in hub_tags:
                if tag.lower() in KEYWORDS:
                    title = post.find('a', class_='post__title_link').text
                    href = post_url
                    posts_list.append({'date': f'{datetime.now()}', 'title': title, 'url': href})
                    tag_exists = True
                    break

            if not tag_exists:
                post_url_response = requests.get(post_url)
                soup_post = BeautifulSoup(post_url_response.text, 'html.parser')
                post_content = soup_post.find(id='post-content-body')
                post_text = post_content.find_all('p')

                text_list = [text_item.text for text_item in post_text]
                text = [text.split() for text in text_list]
                words = []
                for item in text:
                    for word in item:
                        words.append(word)

                for word in words:
                    if word.lower() in KEYWORDS:
                        title = post.find('a', class_='post__title_link').text
                        href = post_url
                        posts_list.append({'date': f'{datetime.now()}', 'title': title, 'url': href})
                        break
    return posts_list


if __name__ == '__main__':
    pprint(scrap_habr_posts(4))
    print('\n\n\n\n')
    pprint(scrap_habr_posts_v2(4))
