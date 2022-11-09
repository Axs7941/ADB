from queue import PriorityQueue
from select import select
from flask import Flask,request,render_template
import pyodbc
from geopy import distance,Nominatim
#from geopy.geocoders import Nominatim
import math

app = Flask(__name__,template_folder='template')


#driver= '{ODBC Driver 17 for SQL Server}'
driver= '{SQL Server}'
server = 'tcp:abhyudai.database.windows.net,1433'
database = 'abhyudai'
username = 'abhyudai'
password = 'HR26m1239#'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


#Homepage Function
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('homepage.html')

#TO PRINT ALL THE DATA 
@app.route('/data',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        cnxn.cursor()   
        cursor.execute("SELECT * FROM all_month")
        rows = cursor.fetchall()
        cursor.connection.commit()
        return render_template('data.html', result=rows)
    return render_template('homepage.html')

#TO FIND MAG N OF EARTHQUAKE FOR TOP N
@app.route('/MagN',methods=['GET','POST'])
def MagN():
    if request.method == 'POST':
        details = request.form
        magN = (details['MagN'])
        cnxn.cursor()   
        cursor.execute("select * from all_month where mag> '"+ magN +"' order by mag desc;")
        rows = cursor.fetchmany(6)#To change  the number of output lines 
        cursor.connection.commit()
        return render_template('data.html', result=rows)
    return render_template('data.html')    

#Calculate Earthquake  by date and magnitude 
@app.route("/earthquakecountbydate",methods=['GET','POST'])
def earthquakecountbydate():
    if request.method == 'POST':
        details = request.form
        dateX = details['DateX1']
        dateY = details['DateY1']
        magofquake = details['MagOfQuake']
        cnxn.cursor()   
        cursor.execute("SELECT * from  all_month WHERE time BETWEEN '"+ dateX +"' AND '"+ dateY +"' and mag > '"+ magofquake +"';")
        rows = cursor.fetchall()#To change  the number of output lines 
        cursor.connection.commit()
        return render_template('data.html', result=rows)
    return render_template('data.html')    

@app.route("/earthquakebydateandmagrange",methods=['GET','POST'])
def earthquakebydateandmagrange():
    if request.method == 'POST':
        details = request.form
        dateX = details['DateX2']
        dateY = details['DateY2']
        magofquake1 = details['MagOfQuake1']
        magofquake2 = details['MagOfQuake2']
        cnxn.cursor()   
        #cursor.execute("SELECT * from  all_month WHERE time BETWEEN '"+ dateX +"' AND '"+ dateY +"' and mag > '"+ magofquake +"';")
        cursor.execute("select * from [dbo].[all_month]where mag between '"+magofquake1 +"' and '"+ magofquake2 +"' and time between '"+dateX+"' and '"+ dateY +"' order by mag desc;")
        rows = cursor.fetchall()#To change  the number of output lines 
        cursor.connection.commit()
        return render_template('data.html', result=rows)
    return render_template('data.html')  


@app.route("/countofearthquakebydateandmagrange",methods=['GET','POST'])
def countearthquakebydateandmagrange():
    if request.method == 'POST':
        details = request.form
        dateX = details['DateX2']
        dateY = details['DateY2']
        magofquake1 = details['MagOfQuake1']
        magofquake2 = details['MagOfQuake2']
        cnxn.cursor()   
        cursor.execute("select count('earthquake') from [dbo].[all_month] where mag between '"+magofquake1 +"' and '"+ magofquake2 +"' and time between '"+dateX+"' and '"+ dateY +"';")
        rows = cursor.fetchall()
        cursor.execute("select count('earthquake') from [dbo].[all_month] where mag between '1' and '2';")
        rows_1_2 = cursor.fetchall()
        cursor.execute("select count('earthquake') from [dbo].[all_month] where mag between '2.1' and '3';")
        rows_2_3 = cursor.fetchall()
        cursor.execute("select count('earthquake') from [dbo].[all_month] where mag between '3.1' and '4';")
        rows_3_4 = cursor.fetchall()
        cursor.execute("select count('earthquake') from [dbo].[all_month] where mag between '4.1' and '5';")
        rows_4_5 = cursor.fetchall()
        cursor.execute("select count('earthquake') from [dbo].[all_month] where mag between '5.1' and '6';")
        rows_5_6 = cursor.fetchall()
        cursor.execute("select count('earthquake') from [dbo].[all_month] where mag between '6.1' and '7';")
        rows_6_7 = cursor.fetchall()
        cursor.execute("select count('earthquake') from [dbo].[all_month] where mag between '7.1' and '8';")
        rows_7_8 = cursor.fetchall()
        cursor.execute("select count('earthquake') from [dbo].[all_month] where mag between '8.1' and '9';")
        rows_8_9 = cursor.fetchall()
        cursor.connection.commit()
        return render_template('test2.html', count=rows,rows_1_2=rows_1_2,rows_2_3=rows_2_3,rows_3_4=rows_3_4,rows_4_5=rows_4_5,rows_5_6=rows_5_6,rows_6_7=rows_6_7,rows_7_8=rows_7_8,rows_8_9=rows_8_9)
    return render_template('test2.html')  
  
@app.route('/placeaffectedbyeartquake',methods=['GET','POST'])#to lat long wokring func
def placeaffectedbyeartquake():
    if request.method == 'POST':
        details = request.form
        place = (details['Place'])
        radius = (details['Radius'])
        name_place_cord= Nominatim(user_agent='get_loc')
        get_loc= name_place_cord.geocode(place)
        lat_current=float(get_loc.latitude)
        long_current=float(get_loc.longitude)
        cnxn.cursor()
        cursor.execute("select * from all_month")
        to_get_lat_long=cursor.fetchall()
        curr_co=(lat_current,long_current)
        row_place=[]
        for i in (to_get_lat_long):
            result_of_quake= (distance.distance(curr_co,(i[1],i[2])).km)
            if result_of_quake <= float(radius):
                row_place.append((i[1],i[2],i[13]))    
        return render_template('data2.html',count=row_place)          
    return render_template('test.html')  

@app.route('/toupdate',methods=['GET','POST'])
def toupdate():
    if request.method == 'POST':
        details = request.form
        magType_current = (details['MagType_update'])
        magType_update = (details['MagType_update'])
        cnxn.cursor()
        cursor.execute("UPDATE all_month SET magType = '"+ magType_current +"' where magType = '"+ magType_update +"'")
        cursor.connection.commit()
        cursor.execute("select * from all_month")
        magType_updated=cursor.fetchall()
        return render_template('data.html',result=magType_updated)          
    return render_template('test.html')  



@app.route("/clusterofearthquake",methods=['GET','POST'])
def clusterofearthquake():
    if request.method == 'POST':
        details = request.form
        latinput = float(details['Latinput'])
        longinput = float(details['Longinput'])
        latup=(math.floor(latinput))
        latdown=(math.ceil(latinput))
        longup=(math.floor(longinput))
        longdown=(math.ceil(longinput))
        cnxn.cursor()   
        cursor.execute("select latitude,longitude from all_month where (latitude between ? and ?) and (longitude between ? and ?)",(latup,latdown,longup,longdown))
        completedata = cursor.fetchall() 
        cursor.connection.commit()
        print(completedata)
        new_row=[]
        for i in (completedata):
            new_row.append((i[0],i[1]))
        return render_template('distance1.html', alllatlong=new_row)
    return render_template('homepage.html')


@app.route("/clusterofearthquake",methods=['GET','POST'])
def clusterofearthquake():
    if request.method == 'POST':
        details = request.form
        latinput = float(details['Latinput'])
        longinput = float(details['Longinput'])
        # latup=(math.floor(latinput))
        # latdown=(math.ceil(latinput))
        # longup=(math.floor(longinput))
        # longdown=(math.ceil(longinput))
        latitudeup = float(latinput) + float(longinput)
        latitudedown = float(latinput) - float(longinput)
        print(latitudeup)
        print(latitudedown)
        cnxn.cursor()   
        cursor.execute("select time, latitude, longitude, mag, id, place from ds4 where longitude  BETWEEN  '"+ str(latitudedown)+"' and '"+str(latitudeup) +"' order by longitude desc;")
        #cursor.execute("select time,latitude,longitude,id, place from ds4 where latitude between '"+ str(latitudeup)+"' and '"+ str(latitudedown)+"' order by longitude desc ;")
        completedata = cursor.fetchall() 
        cursor.connection.commit()
        print(completedata)
        new_row=[]
        for i in (completedata):
            new_row.append((i[0],i[1],i[2],i[3],i[4],i[5]))
        return render_template('distance1.html', alllatlong=new_row)
    return render_template('homepage.html')

#11 ques 
@app.route("/getmaxbymag",methods=['GET','POST'])
def getmaxbymag():
    if request.method == 'POST':
        details = request.form
        column = (details['Column'])
        maghigh = (details['Maghigh'])
        maglow= (details['Maglow'])
        print(column)
        print(maghigh)
        print(maglow)
        cnxn.cursor()   
        row_new=[]
        cursor.execute("select time, latitude, longitude, id, place from ds2 where mag  BETWEEN  '"+ str(maghigh)+"' and '"+str(maglow) +"' and net = '"+ column +"' order by mag desc;")
        completedata = cursor.fetchmany(6) 
        for i in (completedata):
            row_new.append((i[0],i[1],i[2],i[3],i[4]))
            print(completedata)    
        return render_template('distance1.html', alllatlong=row_new)
    return render_template('homepage.html')

@app.route("/toreplacenet",methods=['GET','POST'])
def toreplacenet():
    if request.method == 'POST':
        details = request.form
        netcurrent = (details['Net_current'])
        netupdate = (details['Net_update'])
        print(netcurrent)
        print(netupdate)
        cnxn.cursor()   
        cursor.execute("select count('net') from ds2 where net = '"+ netcurrent+"';")
        netcurrentcount = cursor.fetchall() 
        print(netcurrentcount)
        cursor.execute("update ds2 set  net = '"+ netupdate+"' where net  = '"+ netcurrent+"';")
        #cursor.connection.commit()
        cursor.execute("select count('net') from ds2 where net = '"+ netupdate +"';")
        netupdatecount = cursor.fetchall() 
        cursor.connection.commit()
        print(netupdatecount)
        return render_template('netcount.html', count1=netcurrentcount,count2=netupdatecount)
    return render_template('homepage.html')

@app.route("/toreplacenet",methods=['GET','POST'])
def toreplacenet():
    if request.method == 'POST':
        details = request.form
        netcurrent = (details['Net_current'])
        netupdate = (details['Net_update'])
        print(netcurrent)
        print(netupdate)
        cnxn.cursor()   
        cursor.execute("select count('net') from ds2 where net = '"+ netcurrent+"';")
        netcurrentcount = cursor.fetchall() 
        print(netcurrentcount)
        cursor.execute("update ds2 set  net = '"+ netupdate+"' where net  = '"+ netcurrent+"';")
        #cursor.connection.commit()
        cursor.execute("select count('net') from ds2 where net = '"+ netupdate +"';")
        netupdatecount = cursor.fetchall() 
        #cursor.connection.commit()
        print(netupdatecount)
        return render_template('netcount.html', count1=netcurrentcount,count2=netupdatecount)
    return render_template('homepage.html')

@app.route("/boxplot",methods=['GET','POST'])
def boxplot():
    if request.method == 'POST':
        details = request.form
        latinput1 = float(details['Latinput1'])
        latinput2 = float(details['Latinput2'])
        longinput1 = float(details['Longinput1'])
        longinput2 = float(details['Longinput2'])
        # latup=(math.floor(latinput))
        # latdown=(math.ceil(latinput))
        # longup=(math.floor(longinput))
        # longdown=(math.ceil(longinput))
        cnxn.cursor()   
        cursor.execute("select time,latitude,longitude,id,place from ds2 where (latitude between ? and ?) and (longitude between ? and ?)",(latinput1,latinput2,longinput1,longinput2))
        completedata = cursor.fetchall() 
        cursor.connection.commit()
        new_row=[]
        for i in (completedata):
            new_row.append((i[0],i[1],i[2],i[3],i[4]))
        return render_template('lplusminus.html', longplus=new_row)
    return render_template('cluster.html')    

if __name__== "__app__":
    app.run(debug=True)
