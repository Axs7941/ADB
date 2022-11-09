import re
import string
from flask import Flask, render_template, request,redirect,url_for
from numpy import maximum
import pyodbc
import time
import redis
from typing import List
import pandas as pd
from geopy import distance,Nominatim



#r = redis.StrictRedis(host='resource.redis.cache.windows.net', port=6380, db=0, password='ADB1.redis.cache.windows.net', ssl=True)
r = redis.StrictRedis(host='resource.redis.cache.windows.net',port=6379, db=0, password='JgN4j2DK2KzQDVoMvgNjO3I1WLkDpXTc5AzCaLG4bSw=', ssl=True)

server = 'ganesh.database.windows.net'
database = 'stack'
username = 'ganeshdontha'
password = 'dontha@123'

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#Driver={ODBC Driver 17 for SQL Server};Server=tcp:abhyudai.database.windows.net,1433;Database=abhyudai;Uid=abhyudai;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;


app = Flask(__name__,template_folder='Templates')

@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('homepage.html')

   
@app.route('/alldata', methods=["POST", "GET"])
def alldata():
    if request.method == 'POST':
        start_time = time.time()
        id = 100
        for x in range(id):
            id = id + 1 
            print(id)
            cnxn.cursor()   
            cursor.execute("SELECT * FROM all_month")
            rows = cursor.fetchall()
            cursor.connection.commit()
            timetaken = time.time()-start_time 
        return render_template('data.html', result=rows, Timetaken= timetaken)
    return render_template('homepage.html')


@app.route('/alldatawithredis', methods=["POST", "GET"])
def alldatawithredis():
    if request.method == 'POST':
        start_time = time.time()
        cnxn.cursor()   
        cursor.execute("SELECT * FROM all_month")
        rows = cursor.fetchall()
        cursor.connection.commit()
        r.set('foo', str(rows))
        id = 100
        for x in range(id):
            id = id + 1 
            print(id)
            redisget=r.get('foo')
            timetaken = time.time()-start_time 
            print(timetaken)
        return render_template('datawithredis.html',result=redisget,Timetaken= timetaken)
    return render_template('homepage.html')


@app.route('/databymag', methods=["POST", "GET"])
def databymag():
    if request.method == 'POST':
        start_time = time.time()
        id = 100
        for x in range(id):
            id = id + 1 
            print(id)
            cnxn.cursor()   
            cursor.execute("SELECT mag FROM all_month where mag > 7;")
            rows = cursor.fetchall()
            print(rows)
            cursor.connection.commit()
            timetaken = time.time()-start_time 
        return render_template('data.html', result=rows, Timetaken= timetaken)
        #return('homepage.html')    
    return render_template('homepage.html')

@app.route('/databymagredis', methods=["POST", "GET"])
def databymagredis():
    if request.method == 'POST':
        start_time = time.time()
        cnxn.cursor()   
        cursor.execute("SELECT mag FROM all_month where mag > 7")
        rows = cursor.fetchall()
        cursor.connection.commit()
        id = 10
        r.set('foo', str(rows))
        for x in range(id):
            id = id + 1 
            print(id)
            redisget=r.get('foo')
            timetaken = time.time()-start_time 
            print(timetaken)
        return render_template('datawithredis.html',result=redisget,Timetaken= timetaken)
    return render_template('homepage.html')

@app.route('/createtable',methods=["POST", "GET"] )
def createtable():
    start_time = time.time()
    cursor.execute("CREATE TABLE test (time VARCHAR(200),latitude DECIMAL(15),longitude DECIMAL(15), depth DECIMAL(20),mag DECIMAL(17),magType VARCHAR(10),nst SMALLINT,gap DECIMAL(20),dmin DECIMAL(15),rms DECIMAL(20),net VARCHAR(5),id VARCHAR(20),updated VARCHAR(200),place VARCHAR(100),type VARCHAR(20),horizontalError DECIMAL(20),depthError DECIMAL(20),magError DECIMAL(15) ,magNst SMALLINT,status VARCHAR(15),locationSource VARCHAR(15),magSource VARCHAR(22));")
    cursor.connection.commit()
    #cursor.execute("DROP TABLE test;")
    timetaken = time.time()-start_time 
    print(timetaken)
    return render_template('datawithredis.html', Timetaken=timetaken)   


@app.route('/place_affected_by_eartquake',methods=['GET','POST'])#to lat long wokring func
def place_affected_by_eartquake():
    if request.method == 'POST':
        start_time = time.time()
        details = request.form
        latitude = details['Latitude']
        longitude = details['Longitude']
        radius = details['Radius']
        #name_place_cord= Nominatim(user_agent='get_loc')
        #get_loc= name_place_cord.geocode(place)
        lat_current=float(latitude)
        long_current=float(longitude)
        cnxn.cursor()
        cursor.execute("select * from all_month")
        to_get_lat_long=cursor.fetchall()
        curr_co=(lat_current,long_current)
        row_place=[]
        for i in (to_get_lat_long):
            result_of_quake= (distance.distance(curr_co,(i[1],i[2])).km)
            if result_of_quake <= float(radius):
                row_place.append((i[1],i[2],i[13]))  
                timetaken = time.time()-start_time 
                return render_template('data2.html',count=row_place, Timetaken= timetaken)
        return render_template('data2.html')          
    return render_template('homepage.html')  

@app.route('/place_affected_by_eartquake_redis',methods=['GET','POST'])
def place_affected_by_eartquake_redis()-> str:
    if request.method == 'POST':
        start_time = time.time()    # start_time = time.time()  timetaken = time.time()-start_time
        details = request.form
        latitude = details['Latitude']
        print(latitude)
        longitude = details['Longitude']
        print(longitude)
        radius = details['Radius']
        print(radius)
        lat_current=float(latitude)
        long_current=float(longitude)
        curr_co=(lat_current,long_current)
        cnxn.cursor()
        cursor.execute("select * from all_month")
        to_get_lat_long=cursor.fetchall()
        #print(to_get_lat_long)
        row_place=[]
        for i in (to_get_lat_long):
            result_of_quake= (distance.distance(curr_co,(i[1],i[2])).km)
            if result_of_quake <= float(radius):
                row_place.append((i[1],i[2],i[13]))  
                #(row_place) 
                #print(row_place)
                print("row_place")
                timetaken = time.time()-start_time 
                #return render_template('data.html',Timetaken= timetaken,result=row_place)
                return str(row_place)
           # print(row_place)
            r.set('foo', str(row_place))
            redisget_place=r.get('foo')
            timetaken = time.time()-start_time 
        return render_template('data2.html',result= redisget_place,Timetaken= timetaken)          
    return render_template('homepage.html')  
    
@app.route('/volcanodata',methods=['GET','POST'])
def volcanodata()-> str:
    if request.method == 'POST':
        start_time = time.time()
        cnxn.cursor()
        cursor.execute("select * from volcanoatable")
        allvolcanodata=cursor.fetchall()
        cursor.connection.commit()
        timetaken = time.time()-start_time 
        return render_template('valcanodata.html',result= allvolcanodata,Timetaken=timetaken)


@app.route("/boxplot",methods=['GET','POST'])
def boxplot():
    if request.method == 'POST':
        details = request.form
        elev1 = float(details['Elev1'])
        elev2 = float(details['Elev2'])
        number1 = float(details['Number1'])
        number2 = float(details['Number2'])
        cnxn.cursor()   
        cursor.execute("select min(Elev) as min, max(Elev) as max from volcanoatable where (Elev between ? and ?) and (Number between ? and ?)",(elev1,elev2,number1,number2))
        completedata = cursor.fetchall() 
        cursor.connection.commit()
        new_row=[]
        for i in (completedata):
            # new_row.append((i[0],i[1],i[2],i[3],i[4]))
            new_row.append((i[0],i[1]))
        return render_template('10query.html', longplus=new_row)
    return render_template('home.html')

@app.route("/boxplot2",methods=['GET','POST'])
def boxplot2():
    if request.method == 'POST':
        details = request.form
        elev1 = float(details['Elev1'])
        elev2 = float(details['Elev2'])
        number1 = float(details['Number1'])
        number2 = float(details['Number2'])
        # latup=(math.floor(latinput))
        # latdown=(math.ceil(latinput))
        # longup=(math.floor(longinput))
        # longdown=(math.ceil(longinput))
        cnxn.cursor()   
        cursor.execute("select min(Elev) as min, max(Elev) as max from volcanoatable where (Elev between ? and ?) and (Number between ? and ?)",(elev1,elev2,number1,number2))
        # cursor.execute("select Number,Country,Region,Latitude,Longitude,Elev from vol where (Elev between ? and ?) and (Number between ? and ?)",(elev1,elev2,number1,number2))
        completedata = cursor.fetchall() 
        cursor.connection.commit()
        new_row=[]
        for i in (completedata):
            # new_row.append((i[0],i[1],i[2],i[3],i[4]))
            new_row.append((i[0],i[1]))
        return render_template('10query2.html', longplus=new_row)
    return render_template('cluster.html')

@app.route("/boxplotwithredis",methods=['GET','POST'])
def boxplotwithredis()-> str:
    if request.method == 'POST': # start_time = time.time()  timetaken = time.time()-start_time
        start_time = time.time()
        details = request.form
        elev1 = float(details['Elev1'])
        elev2 = float(details['Elev2'])
        number1 = float(details['Number1'])
        number2 = float(details['Number2'])
        # latup=(math.floor(latinput))
        # latdown=(math.ceil(latinput))
        # longup=(math.floor(longinput))
        # longdown=(math.ceil(longinput))
        cnxn.cursor()   
        cursor.execute("select min(Elev) as min, max(Elev) as max from volcanoatable where (Elev between ? and ?) and (Number between ? and ?)",(elev1,elev2,number1,number2))
        # cursor.execute("select Number,Country,Region,Latitude,Longitude,Elev from vol where (Elev between ? and ?) and (Number between ? and ?)",(elev1,elev2,number1,number2))
        completedata = cursor.fetchall() 
        cursor.connection.commit()
        new_row=[]
        for i in (completedata):
            # new_row.append((i[0],i[1],i[2],i[3],i[4]))
            new_row.append((i[0],i[1]))
            str(new_row)
        r.set('foo', str(new_row))
        id =10
        for i in range(id):
            redisget_place=r.get('foo')
            timetaken = time.time()-start_time
            print(timetaken)
        return render_template('redisdata.html',result=redisget_place,Timetaken=timetaken)
    return render_template('redisdata.html',Timetaken=timetaken)    


@app.route("/votesbyyear",methods=['GET','POST'])
def votesbyyear()-> str:
    if request.method == 'POST': # start_time = time.time()  timetaken = time.time()-start_time
        start_time = time.time()
        details = request.form
        startyear = (details['yearstart'])
        endyear = (details['yearend'])
        voteslow = (details['voteslow'])
        voteshigh = (details['voteshigh'])
        run= int(details['querytime'])
        cnxn.cursor()   
        cursor.execute("select * from votes where year BETWEEN '"+ startyear+"' and '"+ endyear +"' and votes between '"+ voteslow +"' and '"+ voteshigh+"';")
        #cursor.execute("select min(Elev) as min, max(Elev) as max from volcanoatable where (Elev between ? and ?) and (Number between ? and ?)",(elev1,elev2,number1,number2))
        # cursor.execute("select Number,Country,Region,Latitude,Longitude,Elev from vol where (Elev between ? and ?) and (Number between ? and ?)",(elev1,elev2,number1,number2))
        completedata = cursor.fetchall() 
        cursor.connection.commit()
        new_row=[]
        for i in range(run):
            for i in (completedata):
                new_row.append((i[0],i[1],i[2],i[3]))
                timetaken = time.time()-start_time
                print(timetaken)
                return render_template('votesdata.html',result=new_row,Timetaken=timetaken)
            #return render_template('redisdata.html',result=redisget_place,Timetaken=timetaken)
    return render_template('redisdata.html')   

@app.route("/votesbyyearmaxmin",methods=['GET','POST'])
def votesbyyearmaxmin()-> str:
    if request.method == 'POST': # start_time = time.time()  timetaken = time.time()-start_time
        start_time = time.time()
        details = request.form
        startyear = (details['yearstart'])
        endyear = (details['yearend'])
        voteslow = (details['voteslow'])
        voteshigh = (details['voteshigh'])
        run= int(details['querytime'])
        for i in range(run):
            cnxn.cursor()   
            cursor.execute("select votes from votes where year BETWEEN '"+ startyear+"' and '"+ endyear +"' and votes between '"+ voteslow +"' and '"+ voteshigh+"'order by votes desc;")
            maximumvotes = cursor.fetchone() 
            print(maximumvotes)
            cnxn.cursor()   
            cursor.execute("select votes from votes where year BETWEEN '"+ startyear+"' and '"+ endyear +"' and votes between '"+ voteslow +"' and '"+ voteshigh+"'order by votes asc;")
            minimumvotes = cursor.fetchone() 
            print(minimumvotes)
            cursor.connection.commit()
            votes = [maximumvotes,minimumvotes]
            print(votes)
            timetaken = time.time()-start_time
            print(timetaken)
        return render_template('votesmaxmin.html',Timetaken=timetaken,Votes=votes)
            #return render_template('redisdata.html',result=redisget_place,Timetaken=timetaken)
    return render_template('redisdata.html')   

@app.route("/votesbyyearredis",methods=['GET','POST'])
def votesbyyearredis()-> str:
    if request.method == 'POST': # start_time = time.time()  timetaken = time.time()-start_time
        start_time = time.time()
        details = request.form
        startyear = (details['yearstart'])
        endyear = (details['yearend'])
        voteslow = (details['voteslow'])
        voteshigh = (details['voteshigh'])
        run= int(details['querytime'])
        cnxn.cursor()   
        cursor.execute("select * from votes where year BETWEEN '"+ startyear+"' and '"+ endyear +"' and votes between '"+ voteslow +"' and '"+ voteshigh+"';")
        completedata = cursor.fetchall() 
        cursor.connection.commit()
        new_row=[]
        for i in (completedata):
            new_row.append((i[0],i[1],i[2],i[3]))
            print(new_row)
            str(new_row)
            r.set('foo', str(new_row))
            for i in range(run):
                redisget_place=r.get('foo')
                timetaken = time.time()-start_time
                #print(timetaken)
                return render_template('redisdata.html',result=redisget_place,Timetaken=timetaken)
            #return render_template('redisdata.html',result=redisget_place,Timetaken=timetaken)
    return render_template('redisdata.html')    

@app.route("/votesbyyearmaxminredis",methods=['GET','POST'])
def votesbyyearmaxminredis()-> str:
    if request.method == 'POST': # start_time = time.time()  timetaken = time.time()-start_time
        start_time = time.time()
        details = request.form
        startyear = (details['yearstart'])
        endyear = (details['yearend'])
        voteslow = (details['voteslow'])
        voteshigh = (details['voteshigh'])
        run= int(details['querytime'])
        cnxn.cursor()   
        cursor.execute("select votes from votes where year BETWEEN '"+ startyear+"' and '"+ endyear +"' and votes between '"+ voteslow +"' and '"+ voteshigh+"'order by votes desc;")
        maximumvotes = cursor.fetchone() 
        print(maximumvotes)
        cnxn.cursor()   
        cursor.execute("select votes from votes where year BETWEEN '"+ startyear+"' and '"+ endyear +"' and votes between '"+ voteslow +"' and '"+ voteshigh+"'order by votes asc;")
        minimumvotes = cursor.fetchone() 
        print(minimumvotes)
        cursor.connection.commit()
        votes = str([maximumvotes,minimumvotes])
        print(votes)
        r.set('foo', str(votes))
        for i in range(run):
            redisget_votes=r.get('foo')
            timetaken = time.time()-start_time
            print(timetaken)
            return render_template('votesmaxmin.html',Timetaken=timetaken,Votes=redisget_votes)
            #return render_template('redisdata.html',result=redisget_place,Timetaken=timetaken)
    return render_template('redisdata.html')

@app.route("/votesbysum",methods=['GET','POST'])
def votesbysum()-> str:
    if request.method == 'POST': # start_time = time.time()  timetaken = time.time()-start_time
        start_time = time.time()
        details = request.form
        startyear = (details['yearstart'])
        endyear = (details['yearend'])
        run= int(details['querytime'])
        for i in range(run):
            cnxn.cursor()   
            cursor.execute("SELECT SUM(votes),party,state FROM votes where year BETWEEN '"+  startyear +"' and '"+ endyear +"'  group by party,state;")
            votessum = cursor.fetchall() 
            print(votessum)
        # r.set('foo', str(votes))
        # for i in range(run):
        #     redisget_votes=r.get('foo')
            timetaken = time.time()-start_time
        #     print(timetaken)
            return render_template('votessum.html',Votes=votessum)
            #return render_template('redisdata.html',result=redisget_place,Timetaken=timetaken)
    return render_template('redisdata.html')

@app.route("/votesbysumredis",methods=['GET','POST'])
def votesbysumredis()-> str:
    if request.method == 'POST': # start_time = time.time()  timetaken = time.time()-start_time
        start_time = time.time()
        details = request.form
        startyear = (details['yearstart'])
        endyear = (details['yearend'])
        run= int(details['querytime'])
        for i in range(run):
            cnxn.cursor()   
            cursor.execute("SELECT SUM(votes),party,state FROM votes where year BETWEEN '"+  startyear +"' and '"+ endyear +"'  group by party,state;")
            votessum = cursor.fetchall() 
            print(votessum)
            int(votessum)
            r.set('foo', str(votessum))
            for i in range(run):
                redisget_votes=r.get('foo')
                timetaken = time.time()-start_time
                print(timetaken)
                return render_template('votessum.html',Votes=redisget_votes)
            #return render_template('redisdata.html',result=redisget_place,Timetaken=timetaken)
    return render_template('redisdata.html')

@app.route("/votes",methods=['GET','POST'])
def votes():
    if request.method == 'POST':
        USA = request.form
        year1 = USA['Year1']
        year2 = USA['Year2']
        votes1 = USA['Votes1']
        votes2 = USA['Votes2']
        
        cnxn.cursor()   
        cursor.execute("select * from pvotes where (year between ? and ?) and (votes between ? and ?)",(year1,year2,votes1,votes2))
        # cursor.execute("select Number,Country,Region,Latitude,Longitude,Elev from vol where (Elev between ? and ?) and (Number between ? and ?)",(elev1,elev2,number1,number2))
        completedata = cursor.fetchall() 
        cursor.connection.commit()
        new_row=[]
        for i in (completedata):
            new_row.append((i[0],i[1],i[2],i[3]))
            #new_row.append((i[0],i[1]))
        return render_template('question10.html', voting=new_row)
    return render_template('home.html')






if __name__ == '__main__':
    app.run(debug =True)
    