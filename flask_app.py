# A very simple Flask Hello World app for you to get started with...

from flask import Flask

server = Flask(__name__)

####
# Dash app 'app.py'
####

# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import requests
import six.moves.urllib.request as urlreq
import time

VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'adminnn',
    'user': 'user'
}


app = dash.Dash(__name__)


data = html.Div(children=[
	html.Div(
		dcc.Tabs(id='tabs-example', value='гомель', children=[
			dcc.Tab(label='Гомель', value='гомель', className = "tabStyle"),
			dcc.Tab(label='Мозырь', value='мозырь', className = "tabStyle"),
			dcc.Tab(label='Светлогорск', value='светлогорск', className = "tabStyle"),
			dcc.Tab(label='Гомельская область', value='область', className = "tabStyle")
    ], parent_className = "tabzStyle", className = "tabzConteiner")),
    html.Div(children=[
        html.Div(children=[
        	html.Button('Изменить кол-во выводимых столбцов', id='TChange', n_clicks=0, className='SbuttonStyle')
        ], className = 'insider'),
        html.Div(children=[
            dcc.RadioItems(
                id = "Rdd",
                options=[
                    {'label': 'Сортировать по рейтингу', 'value': 'Рейтинг'},
                    {'label': 'Сортировать по ФИО', 'value': 'Фамилия и Имя'},
                    {'label': 'Сортировать по классу', 'value': 'Класс'},
                    {'label': 'Сортировать по дате последнего участия', 'value': 'Дата'}
                ],
                value='Рейтинг'
            )
        ]),
        html.Div(children=[
            html.Button('Изменить вывод учебных заведений', id='ZChange', n_clicks=0, className='SbuttonStyle')
        ], className = 'insider'),
    ], className = 'style1'),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
	            html.Div(dcc.Input(id='Nickname', type='text', placeholder="Никнейм".format('text')), className = "inputStyle"),
	            html.Div(dcc.Input(id='NClass', type='text', placeholder="Класс".format('text'), className = "ninputStyle")),
	            html.Div(dcc.Input(id='UZ', type='text', placeholder="Учебное заведение".format('text')), className = "inputStyle"),
    	        html.Button('Добавить учащегося', id='Add', n_clicks=0, className='buttonStyle')
    	    ], className = 'insider')
    	], hidden = True),
    	html.Div(children=[
    	    html.Div(children=[
        	    html.Div(dcc.Input(id='Button2', type='text', placeholder="Фамилия и имя".format('text')), className = "inputStyle"),
        	    html.Button('Удалить учащегося', id='Remove', n_clicks=0, className='buttonStyle')
        	], className = 'insider')
    	], hidden = True),
    	html.Div(children=[
    	    html.Button('Обновить раунды', id='btn-nclicks-1', n_clicks=0, className='buttonStyle'),
            html.Div(id='container-button-timestamp')
        ], hidden = False),
        html.Div(children=[
            html.Button('Перевести всех в следующий класс', id='Klass', n_clicks=0, className='SbuttonStyle')
        ], hidden = True),
    ], className = "style1"),
    html.Div(id='tabs-example-content', className='divStyle')
], id = 'layout')

app.layout= data



def TChangee(currTab):
    f = open('type.txt', 'r')
    cur = f.read()
    cur = str((int(cur[0]) + 1) % 2) + '\n'
    f.close()
    f = open('type.txt', 'w')
    f.write(cur)
    f.close()



def ZChangee(currTab):
    f = open('zype.txt', 'r')
    cur = f.read()
    cur = str((int(cur[0]) + 1) % 2) + '\n'
    f.close()
    f = open('zype.txt', 'w')
    f.write(cur)
    f.close()



def createTable(tab, rdd):
	f = open('type.txt', 'r')
	cur = f.read(1)
	f.close()
	z = open('zype.txt', 'r')
	zur = z.read(1)
	z.close()
	dataframe = ""
	tabType = 0
	if tab == "область":
		tabType = tabType + 1
		cities = ['гомель', 'мозырь', 'светлогорск']
		curLen = 0
		city = []
		dataframe = pd.read_csv(cities[0] + '.csv')
		while curLen < len(dataframe):
			cities[0] = cities[0][0].upper() + cities[0][1 : len(cities[0])]
			city.append(cities[0])
			curLen = curLen + 1
		for i in range(1, len(cities)):
			dataframe = pd.concat((dataframe, pd.read_csv(cities[i] + '.csv')))
			cities[i] = cities[i][0].upper() + cities[i][1 : len(cities[i])]
			while curLen < len(dataframe):
				city.append(cities[i])
				curLen = curLen + 1
		dataframe['Город'] = city
		dataframe = dataframe[['Рейтинг', 'Город', 'Фамилия и Имя', 'Никнейм', 'Класс', 'Учебное заведение', 'Последний раунд', 'Дата']]
		dataframe.head()
	else:
		dataframe = pd.read_csv(tab + '.csv')
	req = 'https://codeforces.com/api/user.info?handles='
	for i in range(len(dataframe)):
		req = req + dataframe.iloc[i][2 + tabType] + ';'
	response = requests.get(req)
	response = response.json()
	if response["status"] != "OK":
		return html.Div("Ошибка!")
	response = response["result"]
	for i in range(len(dataframe)):
	    if "rating" in response[i]:
	    	dataframe.iat[i,0] = response[i]["rating"]
	if rdd != "Фамилия и Имя":
		dataframe = dataframe.sort_values(rdd, ascending=False)
	else:
	    dataframe = dataframe.sort_values(rdd, ascending=True)
	for i in range(len(dataframe)):
		color = 'grey'
		if dataframe.iloc[i][0] >= 1200:
			color = 'green'
		if dataframe.iloc[i][0] >= 1400:
			color = 'cyan'
		if dataframe.iloc[i][0] >= 1600:
			color = 'blue'
		if dataframe.iloc[i][0] >= 1900:
			color = 'purple'
		if dataframe.iloc[i][0] >= 2100:
			color = 'orange'
		if dataframe.iloc[i][0] >= 2400:
			color = 'red'
		if dataframe.iloc[i][0] >= 3000:
			color = 'black'
		dataframe.iat[i, 1 + tabType] = html.A(dataframe.iloc[i][1 + tabType], href = 'https://codeforces.com/profile/' + dataframe.iloc[i][2 + tabType], style = {'color': color})
	del dataframe['Никнейм']
	Data = []
	for i in range(len(dataframe)):
		d = time.gmtime(int(dataframe.iloc[i][5 + tabType]))
		d = time.strftime("%d.%m.%Y", d)
		Data.append(d)
	del dataframe['Дата']
	dataframe['Дата'] = Data
	if zur == '1':
		del dataframe['Класс']
		del dataframe['Учебное заведение']
	heada = []
	values = []
	if cur == '1':
		del dataframe['Последний раунд']
		del dataframe['Дата']
		cols = int((len(dataframe) + 14) / 15)
		for i in range(min(len(dataframe), 15)):
			mazz = []
			for j in range(i, len(dataframe), 15):
				for col in dataframe.columns:
					mazz.append(dataframe.iloc[j][col])
			values.append(mazz)
		for i in range(cols):
			for col in dataframe.columns:
				heada.append(col)
	else:
		for col in dataframe.columns:
			heada.append(col)
		for i in range(0, len(dataframe), 1):
		    mazz = []
		    for col in dataframe.columns:
		        mazz.append(dataframe.iloc[i][col])
		    values.append(mazz)
	return html.Table([
		html.Thead(
			html.Tr([html.Th(col) for col in heada])
        ),
		html.Tbody([
			html.Tr([
				html.Td(col) for col in row
			]) for row in values
		])
	], className = "tableStyle")


def Addd(currTab, Nickname, NClass, UZ):
    value = str(Nickname)
    if value == "":
        return "Никнейм не был введен"
    value = value.lower()
    response = requests.get('https://codeforces.com/api/user.info?handles=' + Nickname, params = {"lang": "ru"})
    response = response.json()
    webp = urlreq.urlopen("https://codeforces.com/profile/" + Nickname + "?locale=ru").read().decode("utf-8")
    ptrn = '<div style="font-size: 0.8em; color: #777;">'
    text = ""
    name = ""
    for line in webp:
        text = text + line
        pos = text.find(ptrn) + len(ptrn)
    if pos != 43:
        while text[pos] != '<' and text[pos] != ',':
            name = name + text[pos]
            pos = pos + 1
    f = open(currTab + '.csv', 'a')
    x = []
    response = response["result"]
    response = response[0]
    test = open('test.txt', 'a')
    test.write(currTab)
    test.close()
    if "rating" not in response:
        x.append("0")
    else:
        x.append(str(response["rating"]))
    if name == "":
        x.append("Без Имени")
    else:
        spl = name.split(" ")
        name = spl[1] + " " + spl[0]
        x.append(name)
    x.append(Nickname)
    x.append(NClass)
    x.append(UZ)
    f.write(x[0] + ',' + x[1] + ',' + x[2] + ',' + x[3] + ',' + x[4] + ',-,0' '\n')
    f.close()



def Removee(currTab, value):
	value = str(value)
	df = pd.read_csv(currTab + '.csv')
	df = df.loc[df['Фамилия и Имя'] != value]
	df.to_csv(currTab + '.csv', index=False)



def Updatee(currTab):
	cities = ['гомель.csv', 'мозырь.csv', 'светлогорск.csv']
	for city in cities:
		df = pd.read_csv(city)
		for i in range(len(df)):
			time.sleep(1)
			req = "https://codeforces.com/api/user.rating?handle=" + df.iloc[i][2]
			response = requests.get(req)
			response = response.json()
			response = response["result"]
			if len(response) == 0:
				df.iat[i, 5] = "Нигде не участвовал"
				df.iat[i, 6] = 0
			else:
				df.iat[i, 5] = response[len(response) - 1]["contestName"]
				df.iat[i, 6] = response[len(response) - 1]["ratingUpdateTimeSeconds"]
		df.to_csv(city, index=False)



def plusClass(currTab):
	cities = ['гомель.csv', 'мозырь.csv', 'светлогорск.csv']
	for city in cities:
		df = pd.read_csv(city)
		for i in range(len(df)):
			if df.iat[i,3] != ' ' and df.iat[i,3] != '':
				df.iat[i,3] = int(df.iat[i,3]) + 1
		df = df.loc[df['Класс'] != 12]
		df.to_csv(city, index=False)



@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value'),
              Input('Add', 'n_clicks'),
              Input('Remove', 'n_clicks'),
              Input('ZChange', 'n_clicks'),
              Input('TChange', 'n_clicks'),
              Input('btn-nclicks-1', 'n_clicks'),
              Input('Klass', 'n_clicks'),
              Input('Rdd', 'value')],
              [State('Nickname', 'value'),
               State('NClass', 'value'),
               State('UZ', 'value'),
               State('Button2', 'value')])
def render_content(tab, btn1, btn2, btn3, btn4, btn5, btn6, rdd, Nickname, NClass, UZ, value):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'Add' in changed_id:
		Addd(tab, Nickname, NClass, UZ)
	elif 'Remove' in changed_id:
	    Removee(tab, value)
	elif 'ZChange' in changed_id:
	    ZChangee(tab)
	elif 'TChange' in changed_id:
	    TChangee(tab)
	elif 'btn-nclicks-1' in changed_id:
	    Updatee(tab)
	elif 'Klass' in changed_id:
	    plusClass(tab)
	table = createTable(tab, rdd)
	return table



if __name__ == '__main__':
    app.run_server(Debug=True)
