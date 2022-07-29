import sqlite3
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request,redirect,url_for

con=sqlite3.connect('test.db')
cr=con.cursor()
email='rsawebapp@gmail.com'
password='Qwerty@0022'
server=smtplib.SMTP(host='smtp.gmail.com',port=587)
server.starttls()
server.login(email, password)

app=Flask(__name__)

def sendmail(sendTo,sub,msg):
    global server
    m=MIMEMultipart()
    m['From']=email
    m['To']=sendTo
    msg['Subject']=sub
    m.attach(MIMEText(msg,'plain'))
    server.send_message(m)
    del m

@app.route('/')
@app.route('/index')
def index():
    res=requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false')
    res=res.json()
    cur=res[0]["current_price"]

    con=sqlite3.connect('test.db')
    cr.con.cursor()
    query="select * from alarms where alarm="+str(cur)
    ac=cr.execute(query)
    if(len(ac)>0):
        sendmail("client@domain.com","alert","price of bitcoin met the alert set")
    return render_template('index.html')

@app.route('/setalert/')
def setalert():
    return render_template('set.html')

@app.route('/deletealert/')
def deletealert():
    return render_template('delete.html')

@app.route('/showall/')
def showall():
    con=sqlite3.connect('test.db')
    cr.con.cursor()
    query="select * from alarms"
    ac=cr.execute(query)
    for a in ac:
        print(a)
    return render_template('show.html')
    
@app.route('/create',methods=["POST"])
def create():
    con=sqlite3.connect('test.db')
    cr.con.cursor()
    amount=request.form['amount']
    query="insert into alarms values("+str(amount)+")"
    cr.execute(query)
    con.commit()
    return render_template('index.html')

@app.route('/delete',methods=["POST"])
def delete():
    con=sqlite3.connect('test.db')
    cr.con.cursor()
    amount=request.form['amount']
    query="delete from alarms where alarm="+str(amount)
    cr.execute(query)
    con.commit()
    return render_template('index.html')
@app.route('/back/')
def back():
    return render_template('index.html')
    
