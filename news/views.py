# 파이썬 크롤링 출처
# https://everyday-tech.tistory.com/entry/%EC%89%BD%EA%B2%8C-%EB%94%B0%EB%9D%BC%ED%95%98%EB%8A%94-%EB%84%A4%EC%9D%B4%EB%B2%84-%EB%89%B4%EC%8A%A4-%ED%81%AC%EB%A1%A4%EB%A7%81python-2%ED%83%84
import requests
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import response, status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializer
from .models import News
from .serializer import NewsSerializer


def form(request):
    return render(request, 'news.html')


class NewsView(APIView):
    def get(self, request, **kwargs):
        # 입력받아서 실행할 시
        # query = input('검색 키워드를 입력하세요 : ')  # 도도코인
        # news_num = int(input('총 필요한 뉴스기사 수를 입력해주세요(숫자만 입력) : '))

        # 원래 코드
        # query = kwargs.get('keyword')  # 도도코인
        # news_num = 10

        # 쿼리 스트링 시도
        # keyword = kwargs.get('keyword')
        # newses = kwargs.get('news_num')

        # ajax data 시도
        keyword = request.GET.get('keyword')
        newses = int(request.GET.get('news_num'))
        start_num = request.GET.get('start_num')
        print(keyword)
        print(newses)
        print(start_num)
        query = keyword
        query = query.replace(' ', '+')
        news_num = newses

        news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&start={}'

        req = requests.get(news_url.format(query, start_num))
        soup = BeautifulSoup(req.text, 'html.parser')
        news_dict = {}
        idx = 0
        tidx = 0
        cur_page = int(start_num)

        # db에 넣는다고 할때 원래 저장되 있는 것들을 지우기 위한 코드
        # News.objects.all().delete()

        while idx < news_num:
            ### 네이버 뉴스 웹페이지 구성이 바뀌어 태그명, class 속성 값 등을 수정함(20210126) ###
            req = requests.get(news_url.format(query, cur_page))
            print(news_url.format(query, cur_page))
            soup = BeautifulSoup(req.text, 'html.parser')
            table = soup.find('ul', {'class': 'list_news'})
            li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
            area_list = [li.find('div', {'class': 'news_area'}) for li in li_list]
            a_list = [area.find('a', {'class': 'news_tit'}) for area in area_list]
            text_list = [area.find('a', {'class': 'api_txt_lines dsc_txt_wrap'}).text for area in area_list]

            for n in a_list[:min(len(a_list), news_num - idx)]:
                news_dict[idx] = {'title': n.get('title'),
                                  'url': n.get('href'),
                                  'text': text_list[tidx]}

                # tidx는 인덱스가 10개밖에 없어서 10개면 0으로 초기화
                tidx += 1
                idx += 1
                cur_page +=1
                if tidx > 9:
                    tidx = 0
                    # cur_page += 1



            # db에 저장하기 위한 코드
            # news = News(keyword=query, title=n.get('title'), url=n.get('href'))
            # news.save()
            # idx += 1
            # cur_page += 1
            # pages = soup.find('div', {'class': 'sc_page_inner'})
            # next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page)][0].get('href')
            # req = requests.get('https://search.naver.com/search.nav   er' + next_page_url)
            # soup = BeautifulSoup(req.text, 'html.parser')
            # https://wayhome25.github.io/django/2017/04/01/django-ep9-crud/
        # serializer = NewsSerializer(News.objects.filter(keyword=query), many=True)
        print('크롤링 완료')

        return JsonResponse(news_dict, json_dumps_params={'ensure_ascii': False})
