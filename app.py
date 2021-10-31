from flask import Flask, render_template, redirect , request
from timeit import default_timer as timer
import redis

import pyodbc
import textwrap

server = '*'
database = '*'
username = '*'
password = '*'

driver= '{ODBC Driver 17 for SQL Server}'

db_conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
print(db_conn)
cursor = db_conn.cursor()

myHostname = "*"
myPassword = "*"

r = redis.StrictRedis(host=myHostname, port=6380,
                      password=myPassword, ssl=True)

#cursor.close()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/first", methods=["POST","GET"])
def h():

    if request.method=="POST":
         
         
         elev1 = request.form['elev1']
         elev2 = request.form['elev2']

         l1 = int(elev1)
         l2 = int(elev2)

         
         query = "select m.range as 'lat range', count(*) as [number of occurences] from ( select case"
         for i in range(l1,l2,10):
             if(l2-i>5):
                 query=query+" when Latitude between {} and {} then '{} - {}'".format(i,(i+10),i,i+10)
         query=query+" else '{} +' end as range from dbo.quiz4) m group by m.range order by m.range ".format(i+10)

    
         cursor.execute(query)
         data = cursor.fetchall()
         labels = [row[0] for row in data]
         values = [row[1] for row in data]
         return render_template("graph.html",labels=labels,values=values, data=data)
         
         elif(part == 'b'):
             select_sql=("select net , count(*) from dbo.quiz2 group by net;")
             cursor.execute(select_sql)
             data = cursor.fetchall()
             labels = [row[0] for row in data]
             values = [row[1] for row in data]
             
             return render_template("graph.html",labels = labels, values= values , data= data)


    else:
        return render_template("first.html")



@app.route("/second", methods=["POST","GET"])
def h1():
    if request.method=="POST":
         
         num = request.form['num']
        
         select_sql= "select max(Latitude) from v where country like '%{}%';".format(num)
         cursor.execute(select_sql)
         max = cursor.fetchall()
         l2=int(max[0][0])
       
         select_sql2 ="select min(Latitude) from v where country like '%{}%'".format(num)
         cursor.execute(select_sql2)
         min = cursor.fetchall()
         l1 = int(min[0][0])
        
         query = "select m.range as 'lat range', count(*) as [number of occurences] from ( select case"
         for i in range(l1,l2,10):
             if(l2-i>5):
                 query=query+" when Latitude between {} and {} then '{} - {}'".format(i,(i+10),i,i+10)
         query=query+" else '{} +' end as range from v where country like '%{}%') m group by m.range order by m.range ".format(i+10,country)
         data = cursor.execute(query)
         labels = [row[0] for row in data]
         values = [row[1] for row in data]
         return render_template("graph2.html",labels=labels,values=values, data = data)
         
         elif(num == 'b'):
             select_sql=("select net , count(*) from dbo.quiz2 group by net;")
             cursor.execute(select_sql)
             data = cursor.fetchall()
             labels = [row[0] for row in data]
             values = [row[1] for row in data]
             
             return render_template("graph2.html",labels = labels, values= values)
         else:
             return render_template("second.html")


    else:
        return render_template("second.html")

    if request.method=="POST":
        seq = request.form['seq']
        seq1 = request.form['seq1']
        num = request.form['num']
        satvik = request.form['satvik']
        if (num == 'a'):
            select_sql=("select  v.Volcano_Name, v.country ,v.region, v.Latitude, v.Longitude, v.elev from v,vindex where vindex.[Sequence] BETWEEN ? and ? ")
            cursor.execute(select_sql,seq,seq1)
            data = cursor.fetchall()
            return render_template("secondresult.html",result = data)
        elif(num == 'b'):
            select_sql=("select TOP 10 v.Volcano_Name, v.country ,v.region, v.Latitude, v.Longitude, v.elev from v,vindex where vindex.[Sequence] BETWEEN ? and ? ORDER BY RAND()")
            cursor.execute(select_sql,seq,seq1)
            data = cursor.fetchall()
            return render_template("secondresult.html",result = data)
        else:
           return render_template("second.html")
    



@app.route("/fourth", methods=["POST","GET"])
def h2():
    if request.method=="POST":
         elev1 = request.form['elev1']
         elev2 = request.form['elev2']
         
         
         
         
         select_sql=("select cast(number/1000.0 as float ) number,latitude FROM dbo.quiz4 where number between ? and ? ;")
         cursor.execute(select_sql,elev1,elev2)
         data = cursor.fetchall()
         labels = [row[0] for row in data]
         values = [row[1] for row in data]
         return render_template("graph4.html",labels=labels,values=values,data = data)
         
         elif(num == 'b'):
             select_sql=("select net , count(*) from dbo.quiz2 group by net;")
             cursor.execute(select_sql)
             data = cursor.fetchall()
             labels = [row[0] for row in data]
             values = [row[1] for row in data]
             
             return render_template("graph3.html",labels = labels, values= values)
         else:
             return render_template("fourth.html")


    else:
        return render_template("fourth.html")
    if request.method=="POST":
        mag=request.form['mag']
        mag1 = int(mag)
        
        
        start = timer()
        for i in range(mag1):
            select_sql=("select  * from v")
            cursor.execute(select_sql)
            data = cursor.fetchall()


        
        end = timer()
        val = end -  start
        print(val)
            
        return render_template("fourthresult.html",result = val)
        
    else:
        return render_template("fourth.html")

@app.route("/third", methods=["POST","GET"])
def h3():
    if request.method=="POST":
         
         num = request.form['num']
         if(num == 'a'):
             select_sql=("select mag, time2 from dbo.quiz2 ;")
             cursor.execute(select_sql)
             data = cursor.fetchall()
             labels = [row[0] for row in data]
             values = [row[1] for row in data]
             return render_template("graph4.html",labels=labels,values=values,data = data)
         
         elif(num == 'b'):
             select_sql=("select depth,mag  from dbo.quiz2 ;")
             cursor.execute(select_sql)
             data = cursor.fetchall()
             labels = [row[0] for row in data]
             values = [row[1] for row in data]
             
             return render_template("graph4.html",labels = labels, values= values, data= data)
         else:
             return render_template("third.html")


    else:
        return render_template("third.html")

    if request.method=="POST":
        mag=request.form['mag']
        query1 =int(mag)
        if (query1 == 1):
             iter = int(mag)
             cursor.execute("select * from dbo.v ")
             data = cursor.fetchall()
             r.set('earth',str(data))

             start = timer()
             for x in range(0, iter):
                     r.get('earth')
             
             out = r.get('earth')
                   
             end = timer()
             val = end -  start
             print(val)
             
             return render_template("thirdresult.html",result = val)
    else:
        return render_template("third.html")
        




if __name__ == '__main__':
    app.run(debug = True)

