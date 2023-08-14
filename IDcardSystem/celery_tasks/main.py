from celery import Celery
import os

# 读取Django的配置
os.environ["DJANGO_SETTINGS_MODULE"] = "IDcardSystem.settings"
# "redis://127.0.0.1:6379/1"
# 创建celery对象，并指定配置
# app = Celery("celery_demo", backend="redis://127.0.0.1:6379/10")
app = Celery('celery_demo', broker='redis://127.0.0.1:6379/2', backend='redis://127.0.0.1:6379/1')
# app = Celery("celery_demo")
# celery项目配置：worker代理人，指定任务存储到哪里
app.config_from_object('celery_tasks.config')
# 加载可用任务
app.autodiscover_tasks([
    'celery_tasks.sms',
])
