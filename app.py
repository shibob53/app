#from flask import Flask
from flask import Flask, request, jsonify
import time 
#import request
app = Flask(__name__)

listd={}

def c(user):
  #global listd
  listd[user]=1 
def g():
  #global listd
  return len(listd)

@app.route('/home',methods=["POST"])
def home():
  #data = request.get_json()
  #u = data["user"]
  return len(listd)
@app.route('/add', methods=['POST'])
def add():
  data = request.get_json()
  u = data["user"]
  listd[u]=1 
  return "ok"
if __name__ == '__main__':
    app.run(debug=True)
