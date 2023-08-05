from django.http import JsonResponse
from api.models import Persons, Provinces, Cities, Ethnics
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate
from django.core.mail import send_mail  # 导入发送邮件的包
import random


Code = 0  # 验证码，全局变量


def login(request):
    global Code
    print('Code_login', Code)
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print(r_dict)
        username = r_dict['username']
        password = r_dict['password']
        email = r_dict['email']
        code = r_dict['code']
        # 验证码验证
        if Code == code:
            # 邮箱验证
            num_email = User.objects.filter(email=email).count()
            if num_email != 0:
                # 密码验证
                user = authenticate(username=username, password=password)
                if user is not None:
                    Code = 0
                    resp_data = {'item': '登录成功', 'email': email}
                    return JsonResponse(resp_data)
                else:
                    resp_data = {'item': '用户名或密码错误'}
                    return JsonResponse(resp_data)
            else:
                resp_data = {'item': '邮箱不存在'}
                return JsonResponse(resp_data)
        else:
            resp_data = {'item': '验证码错误'}
            return JsonResponse(resp_data)


def register(request):
    global Code
    print('Code_register', Code)
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print(r_dict)
        username = r_dict['username']
        password = r_dict['password']
        email = r_dict['email']
        code = r_dict['code']
        # 核对验证码
        if Code == code:
            num_email = User.objects.filter(email=email).count()
            print('该email是否已注册', num_email)
            # 邮箱未注册
            if num_email == 0:
                Code = 0
                # 创建新用户
                User.objects.create_user(username=username, password=password, email=email)  # create_user() 可以给密码加密
                resp_data = {'item': '注册成功'}
                return JsonResponse(resp_data)
            else:
                resp_data = {'item': '邮箱已注册'}
                return JsonResponse(resp_data)
        else:
            resp_data = {'item': '验证码错误'}
            return JsonResponse(resp_data)


def get_code(request):
    global Code
    if request.method == "GET":
        email = request.GET.get('email')  # 获取用户邮箱
        # 生成验证码
        code = ''
        for i in range(0, 6):
            code += str(random.randint(0, 9))
        print('验证码', code)
        Code = code
        print('Code_code', Code)
        # 发送邮件
        title = 'django发送验证码'  # 邮件标题
        message = "验证码：" + code  # 邮件内容
        email_mine = '343253855@qq.com'  # 发件箱（setting.py中设置的那个）
        email_list = [email]  # 收件人列表
        result = send_mail(title, message, email_mine, email_list)  # result == 1 说明发送成功
        print('发送成功', result == 1)

        # resp_data = {'item': '发送成功'}
        resp_data = {'item': '发送成功', 'code': code}
        return JsonResponse(resp_data)


# 发送persons
def get_persons(request):
    if request.method == "GET":
        page_size = int(request.GET.get('pageSize'))  # 当前页显示条数
        current_page = int(request.GET.get('currentPage'))  # 当前是第几页
        query_fields = ('number', 'name', 'sex', 'ethnic__name', 'birthday', 'city__province__name', 'city__name')  # 搜索栏字段名
        query_params = {}
        for i in query_fields:
            if request.GET.get(i):
                query_params[i] = request.GET.get(i)
        # print('query_params', query_params)
        persons_qs = Persons.objects.filter(**query_params)  # 不定传参，*列表，**字典
        # print('persons_qs', persons_qs)
        total = persons_qs.count()  # 获取数据总条数
        persons_qs = persons_qs[(current_page - 1)*page_size:current_page*page_size].values('id', 'number', 'name', 'sex', 'birthday', 'address', 'city_id', 'ethnic_id', 'city__name', 'ethnic__name', 'city__province__name')
        # 例 Persons.objects.all()[0:5] 表示直接拿到第1到第5条person数据
        print('persons_qs', persons_qs)  # 传给前端的每个对象形式如下：
        # {
        #     'id': '',                        # 不展示，用于删除/修改
        #     'number': '',                    # 展示
        #     'name': '',                      # 展示
        #     'sex': '',                       # 展示
        #     'birthday': '',                  # 展示
        #     'address': '',                   # 展示
        #     'city_id': '',                   # 不展示，用于添加/修改
        #     'ethnic_id': '',                 # 不展示，用于添加/修改
        #     'city__name': '',                # 展示
        #     'ethnic__name': '',              # 展示
        #     'city__province__name': ''       # 展示
        # }

        # 注意：__跨表不仅能在filter里面使用，还可以在values里面用。
        # （1）Persons.objects.filter(city__name='北京市').values()  # 查询 北京市 包含的person（已知城市，查人）
        # print(Persons.objects.filter(name='张三').values('city__name'))  # 验证√
        # （2）Persons.objects.filter(name='张三').values('city__name')  # 查询 张三 所属城市的name（已知人，查城市）
        # print(Persons.objects.filter(city__name='北京市').values())  # 验证√

        resp_data = {'items': list(persons_qs), 'total': total, 'pageSize': page_size, 'currentPage': current_page}
        return JsonResponse(resp_data)


# 添加person
def add_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)  # 前端向后端发送的参数
        print(r_dict)  # 前端传来的对象形式如下：
        # {
        #     'number': '',                    # 保存
        #     'name': '',                      # 保存
        #     'sex': '',                       # 保存
        #     'birthday': '',                  # 保存
        #     'address': '',                   # 保存
        #     'city_id': '',                   # 保存
        #     'ethnic_id': '',                 # 保存
        #     'city__name': '',                #
        #     'city__province__name': ''       #
        # }
        # __name字段只用于前端展示，所以添加/修改时只需操作Persons表原有的7个字段；添加/修改完成后，重新执行get_persons()，会更新__name字段值。
        Persons.objects.create(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic_id=r_dict['ethnic_id'], birthday=r_dict['birthday'], city_id=r_dict['city_id'], address=r_dict['address'])
        person_qs = Persons.objects.all().values('id', 'number', 'name', 'sex', 'birthday', 'address', 'city_id', 'ethnic_id', 'city__name', 'ethnic__name', 'city__province__name').last()
        print('person_qs', person_qs)

        # 注意：__跨表不能用在create和update里面，只能在跨表查询的时候用。
        # （1）Persons.objects.create(number=r_dict['number'], name=r_dict['name'],sex=r_dict['sex'], ethnic__name=r_dict['ethnic'], birthday=r_dict['birthday'], city__name=r_dict['city'], address=r_dict['address'])  # 验证×
        # （2）Persons.objects.filter(id=r_dict['id']).update(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic__name=r_dict['ethnic'], birthday=r_dict['birthday'], city__name=r_dict['city'], address=r_dict['address'])  # 验证×

        resp_data = {'item': list(person_qs)}
        return JsonResponse(resp_data)


# 删除person
def delete_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print(r_dict)  # 前端传来的对象形式如下：
        # {
        #     'id': '',                        # 用于定位
        #     'number': '',                    #
        #     'name': '',                      #
        #     'sex': '',                       #
        #     'birthday': '',                  #
        #     'address': '',                   #
        #     'city_id': '',                   #
        #     'ethnic_id': '',                 #
        #     'city__name': '',                #
        #     'ethnic__name': '',              #
        #     'city__province__name': ''       #
        # }
        person_qs = Persons.objects.filter(id=r_dict['id'])
        person_qs.delete()
        person_qs = person_qs.values('id', 'number', 'name', 'sex', 'birthday', 'address', 'city_id', 'ethnic_id', 'city__name', 'ethnic__name', 'city__province__name')
        print('person_qs', person_qs)
        resp_data = {'item': list(person_qs)}
        return JsonResponse(resp_data)


# 修改person
def update_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print(r_dict)  # 前端传来的对象形式如下：
        # {
        #     'id': '',                        # 不修改，用于定位
        #     'number': '',                    # 修改
        #     'name': '',                      # 修改
        #     'sex': '',                       # 修改
        #     'birthday': '',                  # 修改
        #     'address': '',                   # 修改
        #     'city_id': '',                   # 修改
        #     'ethnic_id': '',                 # 修改
        #     'city__name': '',                #
        #     'ethnic__name': '',              #
        #     'city__province__name': ''       #
        # }
        # __name字段只用于前端展示，所以添加/修改时只需操作Persons表原有的7个字段；添加/修改完成后，重新执行get_persons()，会更新__name字段值。
        person_qs = Persons.objects.filter(id=r_dict['id']).values('id', 'number', 'name', 'sex', 'birthday', 'address', 'city_id', 'ethnic_id', 'city__name', 'ethnic__name', 'city__province__name')
        person_qs.update(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic_id=r_dict['ethnic_id'], birthday=r_dict['birthday'], city_id=r_dict['city_id'], address=r_dict['address'])
        print('person_qs', person_qs)
        resp_data = {'item': list(person_qs)}
        return JsonResponse(resp_data)


# 发送所有省份provinces
def get_provinces(request):
    if request.method == "GET":
        p = Provinces.objects.all().values()
        resp_data = {'items': list(p)}
        return JsonResponse(resp_data)


# 发送所有城市cities
def get_cities(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print(r_dict)
        # province = Provinces.objects.filter(name=r_dict['city__province__name']).first()
        # cities = province.cities_set.all().values()  # 一对多反向查询，两步
        cities = Cities.objects.filter(province__name=r_dict['city__province__name']).values()  # 基于双下划线的跨表查询，一步
        resp_data = {'items': list(cities)}
        return JsonResponse(resp_data)


# 发送所有民族ethnics
def get_ethnics(request):
    if request.method == "GET":
        e = Ethnics.objects.all().values()
        resp_data = {'items': list(e)}
        return JsonResponse(resp_data)



