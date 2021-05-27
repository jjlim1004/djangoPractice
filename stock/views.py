import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import pandas_datareader as wb
import datetime
import matplotlib
import requests
from bs4 import BeautifulSoup
import pandas as pd


matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rest_framework import viewsets

from rest_framework.views import APIView


def stock(request):
    return render(request, 'stock/kospi.html')


class stock_information(APIView):
    def get(self, request, **kwargs):
        # 크롤링을 해서 가져오는 경우
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
                # print(price)
                code = dd.get('id').replace('dd_Item_', '')
                print(code)
                stock_dict[code] = [name, fieldName, price]
                count += 1

        # data = json.dumps(stock_dict)
        # 한글이 유니코드로 출력되지 않도록 json_dumps_params 설정
        return JsonResponse(stock_dict, json_dumps_params={'ensure_ascii': False})

        # # print(all_table.length)
        # dl = all_table[0].find('dl',{'class':'thead'})
        # dt = dl.find('dt')
        # # print(dt.text)
        #
        # #종목 분류 가져오기
        # # for thead in all_table:
        # #     dl = thead.find('dl',{'class':'thead'})
        # #     dt = dl.find('dt')
        # #     fieldName = dt.text
        # #     print(fieldName)
        #
        # tbody = all_table[0].find_all('dl',{'class':'tbody'})
        # name = tbody[0].find('dt').get_text() #종목명
        # dd = tbody[0].find('dd')
        # code = dd.get('id').replace('dd_Item_','') #종목코드
        # price = tbody[0].find('span').get_text().replace(',','') #가격
        # print(name,code,price)


class stock_graph(APIView):
    def get(self, request, **kwargs):
        date = request.GET.get('date')
        print(type(date))
        print(date)

        cur_year = datetime.datetime.now().year
        # print(type(cur_year)) #int
        cur_month = datetime.datetime.now().month
        cur_day = datetime.datetime.now().day

        pd.set_option('precision', 4)

        print()

        start = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
        end = datetime.datetime(cur_year, cur_month, cur_day)
        # start = datetime.datetime(2021, 5, 1)
        # end = datetime.datetime(2021, 5, 14)
        df_null = wb.DataReader("^KS11", "yahoo", start, end)
        df = df_null.dropna()

        kospi_chart = df.Close.plot(style='b')
        kospi_chart.set_title("KOSPI")
        # kospi_chart.set_ylabel("kospi")
        kospi_chart.set_xlabel("date")
        kospi_chart.set_xlim(str(start), str(end))

        # print(df)

        # print("Close Median", df['Close'].median())
        # print(df['Close'].describe())
        # print(df.corr())

        # plt.show()
        plt.savefig("./stock/static/img/kospi.png")
        img_url = '/stock/static/img/kospi.png'
        data = json.dumps({'date': date, 'img_url': img_url})

        # return render(request, 'stock/test.html', {'date': date, 'img_url': img_url})
        # return HttpResponse({'date': date, 'img_url': img_url})

        return HttpResponse(data)
