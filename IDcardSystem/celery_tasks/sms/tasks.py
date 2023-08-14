from celery_tasks.main import app
from time import sleep
from django.core.mail import send_mail  # 发送邮件


@app.task
def send(a, b):
    print('调用开始')
    print(a, b)
    sleep(10)
    print('调用结束')


@app.task
def send_email(email, number):
    print(email, number)
    title = 'celery发送邮件'  # 邮件标题
    message = '查询其征信：' + number  # 邮件内容
    email_mine = '343253855@qq.com'  # 发件箱（setting.py中设置的那个）
    email_list = [email]  # 收件人列表
    send_mail(title, message, email_mine, email_list)
    print('发送成功')
