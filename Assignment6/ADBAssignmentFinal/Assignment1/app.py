from flask import Flask, render_template, request,redirect,url_for
import pyodbc

server = 'abhyudai.database.windows.net'
database = 'abhyudai'
username = 'abhyudai'
password = 'HR26m1239#'

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#Driver={ODBC Driver 17 for SQL Server};Server=tcp:abhyudai.database.windows.net,1433;Database=abhyudai;Uid=abhyudai;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;

app = Flask(__name__,template_folder='templates')


@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('homepage.html')

@app.route('/get_less_5000',methods=["POST", "GET"])
def get_less_5000():
     if request.method == 'POST':
        cnxn.cursor()   
        cursor.execute("select * from people where salary>5000;")
        rows = cursor.fetchall()
        cursor.connection.commit()
        return render_template('salary.html', result=rows)

@app.route('/Update_keyword',methods=["POST","GET"])
def Update_keyword():
     if request.method == 'POST':
        name = request.form['Name']
        print(name)
        keywords= request.form['Keyword']
        print(keywords)
        cnxn.cursor()   
        cursor.execute("UPDATE people SET Keywords = '"+ keywords +"' WHERE Name ='"+ name +"';")
        cursor.connection.commit()
        cursor.execute("select * from people;")
        rows = cursor.fetchall()
        #print(rows)
        return render_template('salary.html', result=rows)
    

@app.route('/Update_Salary',methods=["POST","GET"])
def Update_Salary():
    if request.method == 'POST':
        name = request.form['Name']
        print(name)
        salary= request.form['Salary']
        cnxn.cursor()   
        cursor.execute("UPDATE people SET salary = '"+ salary +"' WHERE Name ='"+ name +"';")
        cursor.connection.commit()
        cursor.execute("select * from people;")
        rows = cursor.fetchall()
        #print(rows)
        return render_template('salary.html', result=rows)



if __name__ == "__main__":
    app.run(debug=True)
