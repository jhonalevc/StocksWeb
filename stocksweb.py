from flask import Flask
from flask import render_template
from flask import url_for
from flask import request


import pandas as pd
import datetime
from sqlalchemy import create_engine

from gevent.pywsgi import WSGIServer
from flask_session import Session



#Database_Connection
user= 'postgres'
password = 'Alejandro123!'
ip = '34.71.5.205'

#Connect to the DB.
engine = create_engine(
    'postgresql+psycopg2://' + user + ':'+ password +'@'+ ip +'/postgres')


portfolio = pd.read_sql(con= engine, sql ="""SELECT * FROM public.portfolio""" )

app = Flask(__name__)
@app.route("/", methods = ['GET','POST'])
def login():
    return render_template('login.html')


@app.route("/show_info",methods = ['GET','POST'])
def show_info():
    email = request.form.get('email')
    password = request.form.get('password')
    #log  -Log in information
    df_login = pd.DataFrame({
        'log_in_time': [datetime.datetime.now()],
        'user':email,
        'password':password       
    })
    df_login.to_sql(con = engine,schema='public',name='log_in',if_exists='append')
    #Display Stocks To Reveiw
    sr = pd.read_sql(con= engine,sql = """SELECT * FROM public.portfolio""")
    sr = sr['Symbol'].to_list()
    return render_template('show_info.html',email =email,sr = sr)



@app.route("/info_stock", methods =['GET','POST'])
def info_stock():
    chosen_stock = request.form.get('chosen_stock')
    query = """
        SELECT * FROM public.exchange
        WHERE symbol =""" + """'""" +  str(chosen_stock) + """'"""
    data_stock = pd.read_sql(con = engine, sql = query)
    data_stock = data_stock.loc[(
        data_stock['run'].dt.time > datetime.time(7,59,59)) &
        (
            data_stock['run'].dt.time < datetime.time(23,59,59)
        ),:]
    data_stock = pd.merge(
        data_stock,
        portfolio,
        left_on = 'symbol',
        right_on = 'Symbol'
    )[['update','price','Quantity']]

    data_stock['value'] = data_stock['price'] * data_stock['Quantity']
    #data_stock = data_stock.loc[(data_stock['update'] == data_stock['update'].min()) | (data_stock['update'] == data_stock['update'].median()) | (data_stock['update'] == data_stock['update'].max()), :]
    most_recent = data_stock.loc[(
            data_stock['update'] == data_stock['update'].max()
        ),'value']
    earliest = data_stock.loc[(
            data_stock['update'] == data_stock['update'].min()
        ),'value']
    earliest_date = data_stock['update'].min().strftime('%Y-%m-%d')
    max_date = data_stock['update'].max().strftime('%Y-%m-%d')

    most_recent_ = "${:0,.2f}".format(most_recent.values[0])
    earliest_ = "${:0,.2f}".format(earliest.values[0])
    
    data_stock['date_'] = data_stock['update'].dt.date
    last_day = data_stock['date_'].drop_duplicates().sort_values(ascending=False).values[1]
    last_day = data_stock[data_stock['date_'] ==last_day]['update'].max()
    last_day_value = data_stock.loc[(data_stock['update'] == last_day),'value'].values[0]
    last_day_value_ = "${:0,.2f}".format(last_day_value)

    x_c = most_recent.values[0] - last_day_value
    qtyty = data_stock['Quantity'].values[0]
    x_C2 = "${:0,.2f}".format(x_c)



    return render_template(
        'info_stock.html',
        most_recent_= most_recent_,
        earliest_ = earliest_,
        earliest_date = earliest_date,
        max_date = max_date,
        last_day_value_ = last_day_value_,
        x_c= x_c,
        qtyty= qtyty,
        x_C2= x_C2)


if __name__ == "__main__":
    print("1")
    #app.run(host="0.0.0.0", debug=True, port=8080)

    SESSION_TYPE = 'filesystem'
    print("2")
    app.config.from_object(__name__)
    print("3")
    sess = Session()
    print("4")
    sess.init_app(app)
    print("5")
    http_server = WSGIServer(('', 8080), app)
    print("6")
    http_server.serve_forever()
    print("7")


