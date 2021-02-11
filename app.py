from flask import Flask,render_template,request
from database import MyDatabase,SQLITE, Alerts,Credentials,Train_schedule
import json
import africastalking

dbms = MyDatabase(SQLITE, dbname='mydb.sqlite')

username = 'test_eric'
api_key = '3e5a23d1f60b23a96c203603075aebdf4e708a4466345d9eb3446284f5e721bc'

africastalking.initialize(username, api_key)
sms = africastalking.SMS

app = Flask(__name__)

@app.route('/create_tables',methods=['POST','GET'])
def create_tables():
    dbms.create_db_tables()
    return ("Done")

@app.route('/sms/<number>/<status>',methods=['POST','GET'])
def sms1(number,status):
    return sms.send(str(status), [number])

@app.route('/',methods=['POST','GET'])
def index():
    credentials = dbms.data_query("Credentials")
    alerts = dbms.data_query("Alerts")[-18:]
    train_schedule = dbms.data_query("Train_schedule")

    for _train_schedule in train_schedule:
        if _train_schedule.passing_status == True:
            LAST_TRAIN = _train_schedule
        else:
            NEXT_TRAIN = _train_schedule

    return render_template('index.html',credentials=credentials,alerts=alerts,NEXT_TRAIN=None ,LAST_TRAIN=  None)

@app.route('/Alerts',methods=['POST'])
def Alerts():
    print(request.data)
    data =json.loads(request.data.decode())
    print(data)
    dbms.sample_insert("Alerts",data)
    return ("")

@app.route('/Credentials',methods=['POST'])
def Credentials():
    data =json.loads(request.data.decode())
    dbms.sample_update("Credentials",data)
    return ({"status":"succesful"})

def update_alerts():
    dbms.sample_update(Alerts)
    # dbms.sample_delete() # delete data
    # dbms.sample_insert() # insert data

if __name__ == "__main__":
    app.run(debug=True,port=4763)
