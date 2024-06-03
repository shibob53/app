from flask import Flask, request, jsonify
import time 
#import request
app = Flask(__name__)

listd={}

def c(user):
  listd[user]=1 
def g():
  return len(listd)
@app.route('/')
def home():
    return g()#"Hello, اتحداك تشغله"
@app.route('/add', methods=['POST'])
def add():
  data = request.get_json()
  u = data["user"]
  c(u)
  return "ok"
if __name__ == '__main__':
    app.run(debug=True)
