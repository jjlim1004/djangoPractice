import json

from django.http import HttpResponse
from django.shortcuts import render
import pandas_datareader as wb
import pandas as pd
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rest_framework import viewsets

from rest_framework.views import APIView


def stock(request):
    return render(request, 'stock/kospi.html')


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
