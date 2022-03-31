# import libraries
from flask import Flask, render_template,request,jsonify
import json
import joblib
from matplotlib.font_manager import json_dump
import util
import os
from datetime import datetime
import pymysql

#db connect
hostname = 'localhost'
username = 'root'
password = ''
database = 'ckd'
myconn = pymysql.connect( host=hostname, user=username, passwd=password, db=database ,cursorclass=pymysql.cursors.DictCursor)
conn = myconn.cursor()

# specify upload folder
UPLOAD_FOLDER = './uploads'

# init flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# login
@app.route('/login', methods=['POST'])
def login():
    try:
        if request.method == 'POST':
            conn.execute("""Select dob from users where mail=%s and password=sha2(%s,256)""",[request.form.get("mail"),request.form.get("password")])
            result=conn.fetchone()
            print(result)
            if(len(result)==0):
                return "error"
            return json.dumps(result,default=str)
    except Exception as e:
        print(e)
        return "error"

# signup
@app.route('/signup', methods=['POST'])
def signup():
    try:
        if request.method == 'POST':
            count=conn.execute("""Insert into users(id,username,mail,dob,password) Values(NULL,%s,%s,%s,sha2(%s,256))""",[request.form.get("username"),request.form.get("mail"),request.form.get("dob"),request.form.get("password")])
            myconn.commit()
            print(count)
            if(count==0):
                return "error"
            return "done"
    except Exception as e:
        print(e)
        return "error"

# to extract values from lab report
@app.route('/extract', methods=['POST'])
def extract():
    if request.method == 'POST':
        if 'pic' not in request.files:
            return "error"
        now=datetime.now()
        file1 = request.files['pic']
        path = os.path.join(app.config['UPLOAD_FOLDER'], now.strftime("%d%m%Y%H%M%S")+file1.filename)
        file1.save(path)
        result=util.extract(path)
        if(result=="error"):
            return "error"
        return json.dumps(result)

# to predict
@app.route('/estimate', methods=['POST'])
def estimate():
    if request.method=="POST":
        age=float(request.form.get("age"))
        bp=float(request.form.get("bp"))
        sg=float(request.form.get("sg"))
        al=float(request.form.get("al"))
        # su=float(request.form.get("su"))
        # rbc=float(request.form.get("rbc"))
        pc=float(request.form.get("pc"))
        pcc=float(request.form.get("pcc"))
        ba=int(request.form.get("ba"))
        bgr=float(request.form.get("bgr"))
        bu=float(request.form.get("bu"))
        sc=float(request.form.get("sc"))
        sod=float(request.form.get("sod"))
        # pot=float(request.form.get("pot"))
        hemo=float(request.form.get("hemo"))
        pcv=float(request.form.get("pcv"))
        wc=float(request.form.get("wc"))
        rc=float(request.form.get("rc"))
        htn=int(request.form.get("htn"))
        dm=int(request.form.get("dm"))
        cad=int(request.form.get("cad"))
        appet=int(request.form.get("appet"))
        pe=int(request.form.get("pe"))
        ane=int(request.form.get("ane"))
        result=util.estimate([age,bp,sg,al,pc,pcc,ba,bgr,bu,sc,sod,hemo,pcv,wc,rc,htn,dm,cad,appet,pe,ane])
    else:
        return "error"
    return result


if __name__ == '__main__':
    # socketio.run(app, debug=True,host="192.168.42.229")
    app.run(debug=True,port=3000,host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'))