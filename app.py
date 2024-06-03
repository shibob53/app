from flask import Flask, request, jsonify
from flask_executor import Executor
import redis
import logging

app = Flask(__name__)
executor = Executor(app)

# إعداد الاتصال ب Redis باستخدام URL من Heroku
#redis_url = "your_actual_redis_url" 
redis_url ="redis://:p5347bec6bfe2865a7483552281f975cfcaa86dd4e13d7d69761ca839d4d8641d@ec2-44-207-232-130.compute-1.amazonaws.com:14739"
#r = redis.Redis.from_url(redis_url)# استبدل هذه القيمة بـ URL الفعلي
redis_client = redis.StrictRedis.from_url(redis_url)

# إعداد تسجيل الأخطاء
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# تسجيل الجلسات في Redis
def save_session(user_id, data):
    redis_client.hset('sessions', user_id, data)

def get_session(user_id):
    return redis_client.hget('sessions', user_id)

# استيراد Blueprints
from user_routes import user_bp

app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/user_count', methods=['GET'])
def user_count():
    user_count = redis_client.hlen('users')
    return jsonify(user_count=user_count)

if __name__ == '__main__':
    app.run(debug=True)
