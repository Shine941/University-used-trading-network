import os

# 0.指定设置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'University_mall.settings')
# 1.创建celery实例
from celery import Celery

app = Celery('celery_tasks')
# 2.设置broker
# 我们可以过加配置文件来设置broker（config)
app.config_from_object('celery_tasks.config')

# 3.需要celery 自动检测指定包的任务
# autodiscover_tasks 参数是列表
# 列表中的元素是 tasks的路径
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
