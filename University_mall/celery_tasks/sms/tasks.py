# 生产者，任务函数
# 发送短信
# 这个函数必须让celery的实例的task装饰器装饰
# 需要celery自动指定报包的人物
from libs.yuntongxun.sms import CCP
from celery_tasks.main import app


@app.task
def celery_send_sms_code(mobile, code):
    CCP().send_template_sms(mobile, [code, 5], 1)
