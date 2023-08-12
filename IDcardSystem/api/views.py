import datetime
from django.http import JsonResponse
from api.models import Persons, Provinces, Cities, Ethnics, Register, Countries
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate
from django.core.mail import send_mail  # 发送邮件
import random
from rest_framework.views import APIView  # 创建类视图
import redis


# ========== 类视图 ==========
# 主页，增删改查
class PersonsView(APIView):
    # “查”，前端发送get请求，携带搜索信息和分页参数
    def get(self, request):
        page_size = int(request.query_params.get('pageSize'))  # 当前页显示条数
        current_page = int(request.query_params.get('currentPage'))  # 当前页是第几页
        query_fields = ('number', 'name', 'sex', 'ethnic__name', 'birthday', 'city__province__name', 'city__name')  # 搜索栏字段名
        query_params = {}
        for i in query_fields:
            if request.query_params.get(i):
                query_params[i] = request.query_params.get(i)
        # print('query_params', query_params)
        persons_qs = Persons.objects.filter(**query_params)  # 不定传参，*列表，**字典
        # print('persons_qs', persons_qs)
        total = persons_qs.count()  # 获取数据总条数
        persons_qs = persons_qs[(current_page - 1) * page_size:current_page * page_size].values('id', 'number', 'name', 'sex', 'birthday', 'address', 'city_id', 'ethnic_id', 'city__name', 'ethnic__name', 'city__province__name')
        # print('persons_qs', persons_qs)
        resp_data = {'items': list(persons_qs), 'total': total, 'pageSize': page_size, 'currentPage': current_page}
        return JsonResponse(resp_data)

    # “增”，前端发送post请求，携带要添加的数据
    def post(self, request):
        r_dict = request.data  # 前端向后端发送的参数
        print(r_dict)
        Persons.objects.create(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic_id=r_dict['ethnic_id'], birthday=r_dict['birthday'], city_id=r_dict['city_id'], address=r_dict['address'])
        person_qs = Persons.objects.all().values('id', 'number', 'name', 'sex', 'birthday', 'address', 'city_id', 'ethnic_id', 'city__name', 'ethnic__name', 'city__province__name').last()
        # print('person_qs', person_qs)

        # ===== celery =====
        # 同步信息到社保局
        # 查征信
        # 查祖上三代
        # after_add_person.delay(pid)

        resp_data = {'item': list(person_qs)[0]}
        return JsonResponse(resp_data)

    # “改”，前端发送put请求，携带修改内容和被修改目标的id，且该id要在url上展示出来
    def put(self, request, pk):
        print(pk)  # 主键，id
        r_dict = request.data
        print(r_dict)
        person_qs = Persons.objects.filter(id=pk).values('id', 'number', 'name', 'sex', 'birthday', 'address', 'city_id', 'ethnic_id', 'city__name', 'ethnic__name', 'city__province__name')
        person_qs.update(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic_id=r_dict['ethnic_id'], birthday=r_dict['birthday'], city_id=r_dict['city_id'], address=r_dict['address'])
        # print('person_qs', person_qs)
        resp_data = {'item': list(person_qs)[0]}
        return JsonResponse(resp_data)

    # “删”，前端发送delete请求，携带被修改目标的id，且该id要在url上展示出来
    def delete(self, request, pk):
        print(pk)  # 主键，id
        person_qs = Persons.objects.filter(id=pk)
        person_qs.delete()
        person_qs = person_qs.values('id', 'number', 'name', 'sex', 'birthday', 'address', 'city_id', 'ethnic_id',
                                     'city__name', 'ethnic__name', 'city__province__name')
        # print('person_qs', person_qs)
        resp_data = {'item': list(person_qs)[0]}
        return JsonResponse(resp_data)


# 注册、邮箱验证
class RegisterView(APIView):
    def get(self, request):
        email = request.query_params.get('email')  # 获取用户邮箱
        # 生成验证码
        code = ''
        for i in range(0, 6):
            code += str(random.randint(0, 9))
        print('验证码', code)
        # 发送邮件
        title = 'django发送验证码'  # 邮件标题
        message = "验证码：" + code  # 邮件内容
        email_mine = '343253855@qq.com'  # 发件箱（setting.py中设置的那个）
        email_list = [email]  # 收件人列表
        result = send_mail(title, message, email_mine, email_list)  # result == 1 说明发送成功
        print('发送成功', result == 1)
        out_time = datetime.datetime.now() + datetime.timedelta(minutes=5)  # 五分钟之后的时间，过期时间
        print('过期时间', out_time, type(out_time), out_time.tzinfo)
        Register.objects.create(email=email, code=code, out_time=out_time)
        resp_data = {'message': '发送成功', 'code': code}
        return JsonResponse(resp_data)

    def post(self, request):
        r_dict = request.data
        print(r_dict)
        username = r_dict['username']
        password = r_dict['password']
        email = r_dict['email']
        code = r_dict['code']
        user_r = Register.objects.filter(email=email).values().last()  # Register表中存的最新的一次获取验证码记录
        print(user_r)
        code_r = user_r['code']  # Register表中存的验证码
        print(code_r)
        out_time = user_r['out_time']  # Register表中存的过期时间
        print('过期时间', out_time, type(out_time), out_time.tzinfo)
        time_now = datetime.datetime.now()  # 当前时间
        # time_now = time_now.replace(tzinfo=pytz.UTC)  # 设置时区
        print('当前时间', time_now, type(time_now), time_now.tzinfo)
        if User.objects.filter(email=email).count() == 0:
            if code == code_r:
                if time_now > out_time:
                    print('验证码过期')
                    resp_data = {'message': '验证码过期', 'code': 40001}
                    return JsonResponse(resp_data)
                else:
                    User.objects.create_user(username=username, password=password, email=email)
                    print('注册成功')
                    resp_data = {'message': '注册成功'}
                    return JsonResponse(resp_data)
            else:
                print('验证码错误')
                resp_data = {'message': '验证码错误'}
                return JsonResponse(resp_data, status=400)
        else:
            print('邮箱已注册')
            resp_data = {'message': '邮箱已注册'}
            return JsonResponse(resp_data)


# redis练习，国家、省份、城市、公民数据缓存
class RedisTestView(APIView):
    def get(self, request):
        # redis连接池
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        print('RedisTestView', r.keys())  # 查看缓存中的所有key

        # 获取前端get请求携带的参数
        country = request.query_params.get('country')
        province = request.query_params.get('province')
        city = request.query_params.get('city')
        # 根据国家选择器的选择结果，查询其名下的所有省份
        if country or country == '':
            if r.llen('provinces'):
                # 如果缓存中已有provinces，先在国家表中根据name查询id，然后在省份表中根据country_id查询所有province
                # print('缓存中的Provinces表：', r.lrange('provinces', 0, -1))
                country_id = ''
                for i in r.lrange('countries', 0, -1):
                    if country == eval(i).get('name'):
                        country_id = eval(i).get('id')
                        break
                # print('当前选择的国家id：', country_id)
                provinces = []
                for i in r.lrange('provinces', 0, -1):
                    if country_id == eval(i).get('country_id'):
                        provinces.append(eval(i))
                print('缓存中的查询结果：', provinces)
            else:
                # 如果缓存中没有provinces，先去数据库中匹配，然后将该省份表的全部数据存入缓存
                provinces = Provinces.objects.filter(country__name=country).values()
                print('ORM查询结果：', list(provinces))
                provinces_all = Provinces.objects.all().values()
                for i in provinces_all:
                    r.rpush('provinces', str(i))
                # print('Provinces表已全部存入redis缓存：', r.lrange('provinces', 0, -1))
            resp_data = {'items': list(provinces)}
            return JsonResponse(resp_data)
        # 根据省份选择器的选择结果，查询其名下的所有城市
        if province or province == '':
            # r.delete('cities')
            if r.llen('cities'):
                # print('缓存中的Cities表：', r.lrange('cities', 0, -1))
                province_id = ''
                for i in r.lrange('provinces', 0, -1):
                    if province == eval(i).get('name'):
                        province_id = eval(i).get('id')
                        break
                # print('当前选择的省份id：', province_id)
                cities = []
                for i in r.lrange('cities', 0, -1):
                    if province_id == eval(i).get('province_id'):
                        cities.append(eval(i))
                print('缓存中的查询结果：', cities)
            else:
                cities = Cities.objects.filter(province__name=province).values()
                print('ORM查询结果：', list(cities))
                cities_all = Cities.objects.all().values()
                for i in cities_all:
                    r.rpush('cities', str(i))
                # print('Cities表已全部存入redis缓存：', r.lrange('cities', 0, -1))
            resp_data = {'items': list(cities)}
            return JsonResponse(resp_data)
        # 根据城市选择器的选择结果，查询其名下的所有公民
        if city or city == '':
            # r.delete('persons')
            if r.llen('persons'):
                # print('缓存中的Persons表：', r.lrange('persons', 0, -1))
                city_id = ''
                for i in r.lrange('cities', 0, -1):
                    if city == eval(i).get('name'):
                        city_id = eval(i).get('id')
                        break
                # print('当前选择的城市id：', city_id)
                persons = []
                for i in r.lrange('persons', 0, -1):
                    if city_id == eval(i).get('city_id'):
                        persons.append(eval(i))
                print('缓存中的查询结果：', persons)
            else:
                persons = Persons.objects.filter(city__name=city).values()
                print('ORM查询结果：', list(persons))
                persons_all = Persons.objects.all().values()
                for i in persons_all:
                    r.rpush('persons', str(i))
                # print('Persons表已全部存入redis缓存：', r.lrange('persons', 0, -1))
            resp_data = {'items': list(persons)}
            return JsonResponse(resp_data)

        # 如果缓存中已经存在countries，就直接从缓存中拿；否则就先从数据库中拿，然后再存入缓存。
        if r.llen('countries'):
            # print('缓存中的Countries表：', r.lrange('countries', 0, -1))
            countries = []
            for i in r.lrange('countries', 0, -1):
                # print(json.loads(i))  # json.loads() 只能将 '{'id': 1, 'name': '中国'}' 单引号str 转换为dict
                # print(eval(i))  # eval() 可以将 "{'id': 1, 'name': '中国'}" 双引号str 转换为dict
                countries.append(eval(i))
            print('缓存中的查询结果：', countries)  # list [{'id': 1, 'name': '中国'}, {'id': 2, 'name': '外国'}]
        else:
            countries = Countries.objects.all().values()
            print('ORM查询结果：', list(countries))  # list [{'id': 1, 'name': '中国'}, {'id': 2, 'name': '外国'}]
            # 将国家数据存入缓存
            for i in countries:
                # print(str(i))
                r.rpush('countries', str(i))
            # print('Countries表已全部存入redis缓存：', r.lrange('countries', 0, -1))
        resp_data = {'items': list(countries)}
        return JsonResponse(resp_data)


# ========== 函数视图 ==========
# 登录
def login(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print(r_dict)
        username = r_dict['username']
        password = r_dict['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            resp_data = {'message': '登录成功'}
            return JsonResponse(resp_data)
        else:
            resp_data = {'message': '用户名或密码错误'}
            return JsonResponse(resp_data)


# 注册
def register(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print(r_dict)
        username = r_dict['username']
        password = r_dict['password']
        email = r_dict['email']
        code = r_dict['code']
        user_r = Register.objects.filter(email=email).values().last()  # Register表中存的最新的一次获取验证码记录
        print(user_r)
        code_r = user_r['code']  # Register表中存的验证码
        print(code_r)
        out_time = user_r['out_time']  # Register表中存的过期时间
        print('过期时间', out_time, type(out_time), out_time.tzinfo)
        time_now = datetime.datetime.now()  # 当前时间
        # time_now = time_now.replace(tzinfo=pytz.UTC)  # 设置时区
        print('当前时间', time_now, type(time_now), time_now.tzinfo)
        if User.objects.filter(email=email).count() == 0:
            if code == code_r:
                if time_now > out_time:
                    print('验证码过期')
                    resp_data = {'message': '验证码过期', 'code': 40001}
                    return JsonResponse(resp_data)
                else:
                    User.objects.create_user(username=username, password=password, email=email)
                    print('注册成功')
                    resp_data = {'message': '注册成功'}
                    return JsonResponse(resp_data)
            else:
                print('验证码错误')
                resp_data = {'message': '验证码错误'}
                return JsonResponse(resp_data, status=400)
        else:
            print('邮箱已注册')
            resp_data = {'message': '邮箱已注册'}
            return JsonResponse(resp_data)


# 获取验证码
def get_code(request):
    if request.method == "GET":
        email = request.GET.get('email')  # 获取用户邮箱
        # 生成验证码
        code = ''
        for i in range(0, 6):
            code += str(random.randint(0, 9))
        print('验证码', code)
        # 发送邮件
        title = 'django发送验证码'  # 邮件标题
        message = "验证码：" + code  # 邮件内容
        email_mine = '343253855@qq.com'  # 发件箱（setting.py中设置的那个）
        email_list = [email]  # 收件人列表
        result = send_mail(title, message, email_mine, email_list)  # result == 1 说明发送成功
        print('发送成功', result == 1)
        out_time = datetime.datetime.now() + datetime.timedelta(minutes=5)  # 五分钟之后的时间，过期时间
        print('过期时间', out_time, type(out_time), out_time.tzinfo)
        Register.objects.create(email=email, code=code, out_time=out_time)
        resp_data = {'message': '发送成功', 'code': code}
        return JsonResponse(resp_data)


# 发送persons
def get_persons(request):
    if request.method == "GET":
        # print(request.GET)
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

        # 同步信息到社保局
        # 查征信
        # 查祖上三代
        # after_add_person.delay(pid)
        resp_data = {'item': list(person_qs)}
        return JsonResponse(resp_data)


# from celery import task
# @task
# def after_add_person(p_id):
#     persion =


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



