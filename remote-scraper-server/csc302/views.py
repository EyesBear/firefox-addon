from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import JsonResponse

import bs4
import requests
import json


def search(query):
    url = 'http://www.amazon.ca/s/ref=nb_sb_noss_2?url=search-alias' \
          '%3Daps&field-keywords={}'.format(query.replace(' ', '+'))
    return scrape(url)


def scrape(url):
    response = requests.get(url,
                            headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                   '6.2; WOW64) AppleWebKit/'
                                                   '537.36 (KHTML, like '
                                                   'Gecko) Chrome/37.0.2062.'
                                                   '120 Safari/537.36'})

    soup = bs4.BeautifulSoup(response.content, "html.parser")
    prod_list = []
    product = {}

    for tag in soup.find_all('li', {'class': 's-result-item'}):
        if (len(tag.find_all('h2')) > 0):
              product['title'] = tag.find_all('h2')[0].string

        by_list = tag.find_all('span',
                               {'class': 'a-size-small '
                                         'a-color-secondary'})
        if len(by_list) > 0:
            if 'by ' in by_list[0].string:
                product['by'] = by_list[1].string
            else:
                product['by'] = ''

        price_list = tag.find_all('span',
                                  {'class': 'a-size-base '
                                            'a-color-price '
                                            's-price a-text-bold'})
        if len(price_list) > 0:
            product['price'] = price_list[0].string

        review_list = tag.find_all('a', {'class': 'a-size-small '
                                                  'a-link-normal '
                                                  'a-text-normal'})
        if len(review_list) > 1:
            product['review'] = review_list[len(review_list)-1].string
        elif len(review_list) > 0:
            product['review'] = review_list[0].string

        stars_list = tag.find_all('span',
                                  {'class': 'a-icon-alt'})
        if len(stars_list) > 0:
            if stars_list[0].string == 'Prime':
                if len(stars_list) > 1:
                    product['stars'] = stars_list[1].string
            else:
                product['stars'] = stars_list[0].string

        prod_url_list = tag.find_all('a',
                                     {'class': 'a-link-normal '
                                               's-access-detail-page  '
                                               'a-text-normal'},
                                     href=True)

        if len(prod_url_list) > 0:
            product['product_url'] = prod_url_list[0]['href']

        img_url_list = tag.find_all('img',
                                    {'class': 's-access-image '
                                              'cfMarker'})

        if len(img_url_list) > 0:
            product['img_url'] = img_url_list[0]['src']

        prod_list.append(product.copy())
    
    return json.dumps(prod_list)

@csrf_exempt
def index(request, query):
    return JsonResponse(search(query),safe=False)
