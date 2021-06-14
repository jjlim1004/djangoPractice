import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import pandas_datareader as pdr
import datetime
import matplotlib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from rest_framework.views import APIView
import matplotlib.pyplot as plt
matplotlib.use('Agg')
# import sys
# import numpy as np
# from ta import add_all_ta_features
# import fastai.tabular
# from fastai import *
# from fastai.tabular import *
# from fastai.tabular.all import *
# from sklearn.metrics import mean_squared_error  # Install error metrics
# from sklearn.linear_model import LinearRegression  # Install linear regression model
# from sklearn.neural_network import MLPRegressor  # Install ANN model
# from sklearn.preprocessing import StandardScaler  # to scale for ann
# import yfinance as yf  # Import library to access Yahoo finance stock data
# import plotly.graph_objs as go  # Import the graph ojbects
# import cufflinks as cf


# from plotly.subplots import make_subplots
# import plotly.express as px


def stock(request):
    return render(request, 'stock/kospi.html')

"""
class stock_predict(APIView):
    def get(self, request, **kwargs):
        print("stock_predict")
        stock_code = request.GET.get('stock_code') + '.KS'
        tickerSymbol = request.GET.get('stock_name')

        cur_year = datetime.datetime.now().year
        cur_month = datetime.datetime.now().month
        cur_day = datetime.datetime.now().day

        # startDate = datetime.datetime.now() - datetime.timedelta(365 * 5)
        startDate = '2016-06-04'
        # endDate = datetime.datetime(cur_year, cur_month, cur_day)
        endDate = '2021-06-04'
        print(startDate)
        print(endDate)

        tickerData = yf.Ticker(stock_code)

        df = tickerData.history(start=startDate, end=endDate)

        date_change = '%Y-%m-%d'

        df['Date'] = df.index

        df['Date'] = pd.to_datetime(df['Date'], format=date_change)

        Dates = df['Date']

        df = add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume", fillna=True)

        # print(df.columns)
        fastai.tabular.add_datepart(df, 'Date', drop='True')
        df['Date'] = pd.to_datetime(df.index.values, format=date_change)

        fastai.tabular.add_cyclic_datepart(df, 'Date', drop='True')

        shifts = [1, 5, 10]

        train_pct = .75

        w = 16
        h = 4

        def CorrectColumnTypes(df):
            for col in df.columns[1:80]:
                df[col] = df[col].astype('float')

            for col in df.columns[-10:]:
                df[col] = df[col].astype('float')

            for col in df.columns[80:-10]:
                df[col] = df[col].astype('category')

            return df

        def CreateLags(df, lag_size):

            shiftdays = lag_size
            shift = -shiftdays
            df['Close_lag'] = df['Close'].shift(shift)
            return df, shift

        def SplitData(df, train_pct, shift):
            train_pt = int(len(df) * train_pct)

            train = df.iloc[:train_pt, :]
            test = df.iloc[train_pt:, :]

            x_train = train.iloc[:shift, 1:-1]
            y_train = train['Close_lag'][:shift]
            x_test = test.iloc[:shift, 1:-1]
            y_test = test['Close'][:shift]

            return x_train, y_train, x_test, y_test, train, test

        def PlotModelResults_Plotly(train, test, pred, ticker, w, h, shift_days, name):

            D1 = go.Scatter(x=train.index, y=train['Close'], name='Train Actual')  # Training actuals
            D2 = go.Scatter(x=test.index[:shift], y=test['Close'], name='Test Actual')  # Testing actuals
            D3 = go.Scatter(x=test.index[:shift], y=pred, name='Our Prediction')  # Testing predction

            # Combine in an object
            line = {'data': [D1, D2, D3],
                    'layout': {
                        'xaxis': {'title': 'Date'},
                        'yaxis': {'title': '$'},
                        'title': name + ' - ' + tickerSymbol + ' - ' + str(shift_days)
                    }}
            # Send object to a figure
            fig = go.Figure(line)
            # fig.show()
            stock_dict = {'stockPredict': fig.to_json()}
            return JsonResponse(stock_dict, json_dumps_params={'ensure_ascii': False})

        def LinearRegression_fnc(x_train, y_train, x_test, y_test):

            lr = LinearRegression()
            lr.fit(x_train, y_train)
            lr_pred = lr.predict(x_test)
            lr_MSE = mean_squared_error(y_test, lr_pred)
            lr_R2 = lr.score(x_test, y_test)
            # print('Linear Regression R2: {}'.format(lr_R2))
            # print('Linear Regression MSE: {}'.format(lr_MSE))

            return lr_pred

            # ANN Function

        def ANN_func(x_train, y_train, x_test, y_test):
            # Scaling data
            scaler = StandardScaler()
            scaler.fit(x_train)
            x_train_scaled = scaler.transform(x_train)
            x_test_scaled = scaler.transform(x_test)

            MLP = MLPRegressor(random_state=1, max_iter=1000, hidden_layer_sizes=(100,), activation='identity',
                               learning_rate='adaptive').fit(x_train_scaled, y_train)
            MLP_pred = MLP.predict(x_test_scaled)
            MLP_MSE = mean_squared_error(y_test, MLP_pred)
            MLP_R2 = MLP.score(x_test_scaled, y_test)

            # print('Muli-layer Perceptron R2 Test: {}'.format(MLP_R2))
            # print('Multi-layer Perceptron MSE: {}'.format(MLP_MSE))

            return MLP_pred

        def CalcProfit(test_df, pred, j):
            pd.set_option('mode.chained_assignment', None)
            test_df['pred'] = np.nan
            test_df['pred'].iloc[:-j] = pred
            test_df['change'] = test_df['Close_lag'] - test_df['Close']
            test_df['change_pred'] = test_df['pred'] - test_df['Close']
            test_df['MadeMoney'] = np.where(test_df['change_pred'] / test_df['change'] > 0, 1, -1)
            test_df['profit'] = np.abs(test['change']) * test_df['MadeMoney']
            profit_dollars = test['profit'].sum()
            # print('Would have made: $ ' + str(round(profit_dollars, 1)))
            profit_days = len(test_df[test_df['MadeMoney'] == 1])
            # print('Percentage of good trading days: ' + str(round(profit_days / (len(test_df) - j), 2)))

            return test_df, profit_dollars
            # Go through each shift....

        for j in shifts:
            # print(str(j) + ' days out:')
            # print('------------')
            df_lag, shift = CreateLags(df, j)
            df_lag = CorrectColumnTypes(df_lag)
            x_train, y_train, x_test, y_test, train, test = SplitData(df, train_pct, shift)

            # Linear Regression
            # print("Linear Regression")
            lr_pred = LinearRegression_fnc(x_train, y_train, x_test, y_test)
            test2, profit_dollars = CalcProfit(test, lr_pred, j)
            PlotModelResults_Plotly(train, test, lr_pred, tickerSymbol, w, h, j, 'Linear Regression')
"""

class stock_detail(APIView):
    def get(self, request, **kwargs):
        # https://chancoding.tistory.com/116?category=846070
        # #start를 위해 가져올 날짜 설정
        date = request.GET.get('date')
        print(date)
        stock_code = request.GET.get('stock_code') + '.KS'
        print(stock_code)
        stock_name = request.GET.get('stock_name')
        print(stock_name)

        cur_year = datetime.datetime.now().year
        cur_month = datetime.datetime.now().month
        cur_day = datetime.datetime.now().day

        start = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
        end = datetime.datetime(cur_year, cur_month, cur_day)

        # 야후에서 삼성전자 데이터 가져오기
        stock = pdr.get_data_yahoo(stock_code, start, end)
        # plot = stock.iplot(asFigure=True, title=stock_name, xTitle='날짜', yTitle='거래량')
        plot = stock.iplot(asFigure=True, title=stock_name, xTitle='date', yTitle='volume')
        plot.to_json()
        stock_dict = {'stockGraph': plot.to_json()}
        return JsonResponse(stock_dict, json_dumps_params={'ensure_ascii': False})


class stock_information(APIView):
    def get(self, request, **kwargs):
        # 크롤링을 해서 가져오는 경우
        stock_dict = {}
        query = request.GET.get('query')
        print(query)
        url = 'http://www.sedaily.com/Stock/Quote?type=' + query
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
            # print(fieldName)
            # print(dt)
            tbody = thead.find_all('dl', {'class', 'tbody'})

            count = 0

            for dl in tbody:
                name = dl.find('dt').get_text()
                # print(name)
                dd = dl.find('dd')
                price = tbody[count].find('span').get_text().replace(',', '')
                # print(price)
                code = dd.get('id').replace('dd_Item_', '')

                # print(code)
                stock_dict[code] = [name, fieldName, price]
                count += 1

        # data = json.dumps(stock_dict)

        # sorting test
        # sorted_dict = sorted(stock_dict.items())
        # sorted_dict.sort(key=lambda x: x[1][1])
        # # print(sorted_dict)
        # stock_dict = dict(sorted_dict)
        # print(stock_dict)

        # 한글이 유니코드로 출력되지 않도록 json_dumps_params 설정
        # return JsonResponse(stock_dict, json_dumps_params={'ensure_ascii': False})
        return JsonResponse(stock_dict, json_dumps_params={'ensure_ascii': False})


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

        start = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
        end = datetime.datetime(cur_year, cur_month, cur_day)
        # start = datetime.datetime(2021, 5, 1)
        # end = datetime.datetime(2021, 5, 14)
        df_null = pdr.DataReader("^KS11", "yahoo", start, end)
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
