from django.http import HttpResponse
from django.shortcuts import render
import pandas_datareader as wb
import pandas as pd
import datetime
import matplotlib.pyplot as plt


# Create your views here.
def stock(request):
    return render(request, 'stock/kospi.html')


def kospi(request):
    date = request.GET.get('date')
    # print(type(date)) #str
    cur_year = datetime.datetime.now().year
    # print(type(cur_year)) #int
    cur_month = datetime.datetime.now().month
    cur_day = datetime.datetime.now().day

    pd.set_option('precision', 4)

    start = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
    end = datetime.datetime(cur_year, cur_month, cur_day)
    # start = datetime.datetime(2021, 5, 1)
    # end = datetime.datetime(2021, 5, 14)
    df_null = wb.DataReader("^KS11", "yahoo", start, end)
    df = df_null.dropna()

    kospi_chart = df.Close.plot(style='b')
    kospi_chart.set_title("KOSPI")
    kospi_chart.set_ylabel("코스피 지수")
    kospi_chart.set_xlabel("일자")
    kospi_chart.set_xlim(str(start), str(end))

    # print(df)

    # print("Close Median", df['Close'].median())
    # print(df['Close'].describe())
    # print(df.corr())

    # plt.show()
    plt.savefig("./stock/static/img/kospi.png")

    return render(request, 'stock/test.html', {'date': date, })
