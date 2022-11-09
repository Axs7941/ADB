#from __future__ import division
from flask import Flask, render_template, request,redirect,url_for
import pyodbc 
import json

server = 'ganesh.database.windows.net'
database = 'stack'
username = 'ganeshdontha'
password = 'dontha@123'

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#Driver={ODBC Driver 17 for SQL Server};Server=tcp:abhyudai.database.windows.net,1433;Database=abhyudai;Uid=abhyudai;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;

app = Flask(__name__,template_folder='templates')

@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('homepage.html')


@app.route('/partitionbymag1', methods=["POST", "GET"])#static
def partitionbymags():
    if request.method == 'POST':
        details = request.form
        partition = float(details['Partition'])
        magRangemax = details['MagRangemax']
        magRangelow = details['MagRangelow']
        rows1=[]
        first=round(int((float(magRangemax)-float(magRangelow))/partition))
        print(first)
        cnxn.cursor()
        magcount=magRangelow  
        for i in range(int(partition)):
           magRangelow=str(magcount)
           magcount=str(int(magRangelow)+first) 
           cursor.execute("select count(*) from data-2 where column2 between '"+ magRangelow +"' and '"+ magcount +"';")
           rows2 = cursor.fetchall()
           rows1.append(rows2[0][0])
           print(rows2)
           cursor.connection.commit()
        return render_template('horizontalbarchart.html', result1=json.dumps(rows1))
    return render_template('homepage.html')

@app.route('/scatter', methods=["POST", "GET"])
def scatter():
    if request.method == "POST":
        if request.form.get("fbutton"):
            val1 = request.form["val1"]
            val2 = request.form["val2"]
            cursor = cnxn.cursor()
            cursor.execute("select column1 as x,column3 as y FROM data-2 where column1 between "+val1+" and "+val2+";")
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            results = []
            for row in data:
                results.append(dict(zip(columns, row)))
            return render_template('scatter.html', scatter=results)
        else:
            return render_template('scatter.html')
    else:
        return render_template('scatter.html')


@app.route("/barchart" , methods=['GET','POST'])
def barchart():
    if request.method == 'POST':
        details = request.form
        partition = float(details['Partition'])
        rows1=[]
        rows2=[]
        rows3=[]
        rows4=[]
        cursor.execute("select column4, count(*) as tot from data-2 group by column4 order by tot desc;")
        rows3 = cursor.fetchmany(int(partition))
        for i in range(int(partition)):
         rows1.append(rows3[i][0])
         i=i+1
        print(rows1)
        cursor.execute("select count(*) as tot from data-2 group by column4 order by tot desc;")
        rows4 = cursor.fetchmany(int(partition))
        for i in range(int(partition)):
         rows2.append(rows4[i][0])
         i=i+1
        print(rows2)
        return render_template('horizontalbarchart.html',mag_total=json.dumps(rows1),mag_total2=json.dumps(rows2))
    return render_template('horizontalbarchart.html',mag_total=json.dumps(rows1),mag_total2=json.dumps(rows2))

@app.route('/partitionbymag', methods=["POST", "GET"])#static
def partitionbymag():
    if request.method == 'POST':
        details = request.form
        partition = float(details['Partition'])
        magRangemax = float(details['MagRangemax'])
        phrase_to_list = magRangemax.split()
        print(phrase_to_list)
        rows1=[]
        cnxn.cursor() 
        for i in phrase_to_list:
            ro=str(i) 
            cursor.execute("select count(column4) from data-2 where column4 like'"+ ro +"';")
            rows2 = cursor.fetchall()
            rows1.append(rows2[0][0])
            print(rows2)
            cursor.connection.commit()
        return render_template('piechart.html', result1=json.dumps(rows1))
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug =True)
    