from flask import render_template, redirect, request, url_for, flash, abort
# from flask_login import login_user, logout_user, login_required
from myproject import app, db
# from myproject.models import User
# from myproject.forms import LoginForm, RegistrationForm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mqtt_data.db'
db = SQLAlchemy(app)

# 定义模型用于存储 MQTT 数据


class MQTTData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(17))
    errCode = db.Column(db.String(4))
    product = db.Column(db.String(50))
    message = db.Column(db.String(255))
    command = db.Column(db.String(20))
    params = db.Column(db.JSON)

# MQTT 消息处理函数


def on_mqtt_message(client, userdata, message):
    # 解析消息内容
    topic_array = message.topic.split('/')
    payload = json.loads(message.payload.decode('utf-8'))
    # 创建 MQTTData 对象并存入数据库
    mqtt_data = MQTTData(mac=payload['mac'], errCode=payload['errCode'], product=payload['product'],
                         message=payload['message'], command=payload['command'], params=payload['params'])
    db.session.add(mqtt_data)
    db.session.commit()


# 初始化 MQTT 客户端并连接到 MQTT 代理
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_mqtt_message
mqtt_client.connect('mqtt.example.com', 1883)

# 订阅主题
mqtt_client.subscribe('DAE/fengchia/read')

# 启动 MQTT 客户端循环
mqtt_client.loop_start()

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)
