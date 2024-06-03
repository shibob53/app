from flask import Flask, request
import redis

app = Flask(__name__)

# إعداد الاتصال ب Redis
redis_url ="redis://:p5347bec6bfe2865a7483552281f975cfcaa86dd4e13d7d69761ca839d4d8641d@ec2-44-207-232-130.compute-1.amazonaws.com:14739"
r = redis.Redis.from_url(redis_url)

def c(user):
    r.set(user, "1"+user)

def g(u):
    return r[u]#.keys()

@app.route('/home', methods=["POST"])
def home():
    data = request.get_json()
    u = data["user"]
    return g(u)

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    u = data["user"]
    c(u)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
