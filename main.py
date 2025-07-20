import requests
from bs4 import BeautifulSoup
import time
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'


def generate_headers():
    """Генерирует случайные заголовки для запросов"""
    return Headers(
        browser="chrome",
        os="win"
    ).generate()


def main():
    # Получаем список статей с главной страницы
    response = requests.get(URL, headers=generate_headers())
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    results = []

    for article in articles:
        # Извлекаем базовую информацию
        time_tag = article.find('time')
        if not time_tag:
            continue

        date = time_tag['datetime'][:10]
        title_tag = article.find('h2').find('a')
        title = title_tag.text.strip()
        relative_link = title_tag['href']
        link = f'https://habr.com{relative_link}'

        # Проверка preview-информации
        preview_text = get_preview_text(article).lower()
        if contains_keyword(preview_text, KEYWORDS):
            results.append((date, title, link))
            continue

        # Если в preview не найдено, анализируем полный текст
        try:
            full_text = get_full_article_text(link).lower()
            if contains_keyword(full_text, KEYWORDS):
                results.append((date, title, link))
        except Exception as e:
            print(f"Ошибка при обработке статьи {link}: {str(e)}")

        # Вежливая задержка между запросами дабы не загружать сервер
        time.sleep(0.5)

    # Вывод результатов
    for date, title, link in results:
        print(f"{date} – {title} – {link}")


def get_preview_text(article):
    """Извлекает preview-информацию со страницы списка статей"""
    title = article.find('h2').text.strip()
    hubs = ' '.join(
        hub.text.strip()
        for hub in article.find_all('a', class_='tm-article-snippet__hubs-item-link')
    )
    preview = article.find('div', class_='article-formatted-body')
    preview_text = preview.text.strip() if preview else ''
    return f"{title} {hubs} {preview_text}"


def get_full_article_text(article_url):
    """Получает полный текст статьи по URL"""
    response = requests.get(article_url, headers=generate_headers())
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем основной контент
    title = soup.find('h1')
    title_text = title.text.strip() if title else ''

    hubs = ' '.join(
        hub.text.strip()
        for hub in soup.find_all('a', class_='tm-article-snippet__hubs-item-link')
    )

    # Обрабатываем разные форматы статей
    body = soup.find('div', class_='article-formatted-body') or soup.find('div', class_='tm-article-body')
    body_text = body.text.strip() if body else ''

    return f"{title_text} {hubs} {body_text}"


def contains_keyword(text, keywords):
    """Проверяет наличие хотя бы одного ключевого слова в тексте"""
    return any(keyword in text for keyword in keywords)


if __name__ == '__main__':
    main()