# 파이썬 크롤링 출처
# https://everyday-tech.tistory.com/entry/%EC%89%BD%EA%B2%8C-%EB%94%B0%EB%9D%BC%ED%95%98%EB%8A%94-%EB%84%A4%EC%9D%B4%EB%B2%84-%EB%89%B4%EC%8A%A4-%ED%81%AC%EB%A1%A4%EB%A7%81python-2%ED%83%84
import requests
from bs4 import BeautifulSoup
import re

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import response, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializer
from .models import News
from .serializer import NewsSerializer


def form(request):
    stock_dict = {}

    url = 'http://www.sedaily.com/Stock/Quote?type=1'
    try:
        html = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        soup = BeautifulSoup(html.text, 'lxml')

    all_table = soup.find_all('div', {'class': 'table'})

    for thead in all_table:
        dl = thead.find('dl', {'class': 'thead'})
        dt = dl.find('dt')
        fieldName = dt.text
        #     print(fieldName)
        #     print(dt)
        tbody = thead.find_all('dl', {'class', 'tbody'})

        count = 0
        for dl in tbody:
            name = dl.find('dt').get_text()
            dd = dl.find('dd')
            price = tbody[count].find('span').get_text().replace(',', '')
            print(price)
            code = dd.get('id').replace('dd_Item_', '')
            stock_dict[code] = [name, fieldName, price]
            count += 1

    # # print(all_table.length)
    # dl = all_table[0].find('dl',{'class':'thead'})
    # dt = dl.find('dt')
    # # print(dt.text)

    # #종목 분류 가져오기
    # # for thead in all_table:
    # #     dl = thead.find('dl',{'class':'thead'})
    # #     dt = dl.find('dt')
    # #     fieldName = dt.text
    # #     print(fieldName)

    # tbody = all_table[0].find_all('dl',{'class':'tbody'})
    # name = tbody[0].find('dt').get_text() #종목명
    # dd = tbody[0].find('dd')
    # code = dd.get('id').replace('dd_Item_','') #종목코드
    # price = tbody[0].find('span').get_text().replace(',','') #가격
    # print(name,code,price)

    return render(request, 'news.html')

class NewsView(APIView):
    def get(self, request, **kwargs):
        #입력받아서 실행할 시
        # query = input('검색 키워드를 입력하세요 : ')  # 도도코인
        # news_num = int(input('총 필요한 뉴스기사 수를 입력해주세요(숫자만 입력) : '))
        
        #원래 코드
        # query = kwargs.get('keyword')  # 도도코인
        # news_num = 10

        # 쿼리 스트링 시도
        # keyword = kwargs.get('keyword')
        # newses = kwargs.get('news_num')
        
        #ajax data 시도
        keyword = request.GET.get('keyword')
        newses = int(request.GET.get('news_num'))
        print("news view get")

        print(keyword)
        print(newses)
        query = keyword
        query = query.replace(' ', '+')
        print(query)
        news_num = newses

        news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'

        req = requests.get(news_url.format(query))
        print(news_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        # news_dict = {}
        idx = 0
        cur_page = 1

        print('크롤링 중...')

        News.objects.all().delete()
        while idx < news_num:
            ### 네이버 뉴스 웹페이지 구성이 바뀌어 태그명, class 속성 값 등을 수정함(20210126) ###

            table = soup.find('ul', {'class': 'list_news'})
            li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
            area_list = [li.find('div', {'class': 'news_area'}) for li in li_list]
            a_list = [area.find('a', {'class': 'news_tit'}) for area in area_list]

            for n in a_list[:min(len(a_list), news_num - idx)]:
                # news_dict[idx] = {'title': n.get('title'),
                #                   'url': n.get('href')}
                # idx += 1

                # news_dict[n.get('title')] = n.get('href')
                # idx += 1

                news = News(keyword=query, title=n.get('title'), url=n.get('href'))
                news.save()
                idx += 1


            # https://wayhome25.github.io/django/2017/04/01/django-ep9-crud/
            cur_page += 1

            pages = soup.find('div', {'class': 'sc_page_inner'})
            next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page)][0].get('href')

            req = requests.get('https://search.naver.com/search.naver' + next_page_url)
            soup = BeautifulSoup(req.text, 'html.parser')
        print('크롤링 완료')
        serializer= NewsSerializer(News.objects.filter(keyword=query), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
