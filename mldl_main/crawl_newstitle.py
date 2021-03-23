import requests
from bs4 import BeautifulSoup

def crawl_newstitle(query):

    url = "https://search.naver.com/search.naver?where=news&query=" + query
    web = requests.get(url).content
    source = BeautifulSoup(web, 'html.parser')

    news_subjects = source.find_all('a', {'class' : 'news_tit'})

    list_subject = []
    list_urls = []

    for subject in news_subjects:
        list_subject.append(subject.get_text())
        list_urls.append(subject.attrs['href'])

    return list_subject, list_urls
