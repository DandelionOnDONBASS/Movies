import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from .models import Genre
from django.shortcuts import render, redirect
translator = Translator()

def Genres_add(request):
    cookies = {
        'PHPSESSID': '803c22612126be3966ab37f52a297b7a',
    }

    headers = {
        'authority': 'kinogo.inc',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
        'cache-control': 'max-age=0',
        # 'cookie': 'PHPSESSID=803c22612126be3966ab37f52a297b7a',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    response = requests.get('https://kinogo.inc/', cookies=cookies, headers=headers)

    

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    genres_div = soup.find('div', class_='leftblok1')
    genre_links = genres_div.find_all('a')

    for link in genre_links:
        # english_name = link['href'].replace('/', '')
        genre, created = Genre.objects.update_or_create(
            name=link.text,
            description=link.text,
            url=link['href'].replace('/', ''),
        )
        if created:
            genre.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))