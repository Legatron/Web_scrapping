import requests
import bs4
import fake_headers

headers_generator = fake_headers.Headers(
    os = "win",
    browser="chrome",
)

main_page_response = requests.get(
    "https://habr.com/ru/articles/",
     headers=headers_generator.generate()
)
main_soup = bs4.BeautifulSoup(main_page_response.text, features="lxml" )

article_div_tag = main_soup.find( 'div', class_ = 'tm-articles-list')
article_tags = article_div_tag.find_all('article')
articles = []
for article_tag in article_tags:
    time_tag = article_tag.find("time")
    h2_teg = article_tag.find("h2")
    a_teg = h2_teg.find("a")
    span_teg = a_teg.find("span")

    publication_time = time_tag("datetime")
    relative_article_link = a_teg["href"]
    absolute_article_link = f"https://habr.com{relative_article_link}"
    article_title = span_teg.text.strip()
    article_hhtp_response = requests.get(
        absolute_article_link,
        headers=headers_generator.generate()
    )
    article_html = article_hhtp_response.text
    article_soup = bs4.BeautifulSoup(article_html, features="lxml" )
    article_div_tag = article_soup.find("div", id="post-content-body")
    article_text = article_div_tag.text.strip()
    article_dict = {
        "publication_time": publication_time,
        "absolute_article_link": absolute_article_link,
        "article_title": article_title,
        "article_text": article_text[:100]
    }
    articles.append(article_dict)


print(articles)