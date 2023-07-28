from django.http import JsonResponse
from django.shortcuts import render

from api.models import Persons, Provinces, Cities, Ethnics
import json


# 发送persons
def persons(request):
    # 基础版
    if request.method == "GET":
        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)
    # 分页版
    if request.method == "POST":
        r_dict = json.loads(request.body)
        # print('persons从前端发送来的数据', r_dict)
        print('pageSize与currentPage分别为', r_dict['pageSize'], r_dict['currentPage'])
        p = r_dict['pageSize']  # pageSize，每页显示条数
        c = r_dict['currentPage']  # currentPage，当前页码
        u = []  # 存储当前范围的persons信息

        user_qs = Persons.objects.all().values()
        print(user_qs[0], type(user_qs[0]))  # 验证user_qs的第一个数据是什么样的，字典
        for i in range(0, len(user_qs)):
            if (c - 1)*p <= i < c*p:
                u.append(user_qs[i])
        print(u, len(u))

        # 替换掉三个_id字段
        for i in range(0, len(u)):
            print(u[i], u[i]['ethnic_id'], u[i]['province_id'], u[i]['city_id'])
            e_obj = Ethnics.objects.filter(id=u[i]['ethnic_id']).values()
            p_obj = Provinces.objects.filter(id=u[i]['province_id']).values()
            c_obj = Cities.objects.filter(id=u[i]['city_id']).values()
            print(e_obj[0]['ethnic'], p_obj[0]['province'], c_obj[0]['city'])

            del u[i]['ethnic_id']  # 删除字段
            del u[i]['province_id']
            del u[i]['city_id']
            u[i]['ethnic'] = e_obj[0]['ethnic']  # 添加字段
            u[i]['province'] = p_obj[0]['province']
            u[i]['city'] = c_obj[0]['city']
            print(u[i])  # 将三个_id字段替换是为了与前端表格中的字段对应，方便展示。结果如下：
            # {
            #  'id': 6,
            #  'number': '2435',
            #  'name': '肥肉',
            #  'sex': 1,
            #  'birthday': datetime.date(2023, 7, 11),
            #  'address': '王斐然',
            #  'ethnic': '回族',
            #  'province': '内蒙古自治区',
            #  'city': '通辽市'
            # }

        resp_data = {'items': u}
        return JsonResponse(resp_data)


# 添加person
def add_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)  # 前端向后端发送的参数
        print('add从前端发送来的数据：', r_dict, r_dict['number'])

        e_obj = Ethnics.objects.filter(ethnic=r_dict['ethnic']).first()
        p_obj = Provinces.objects.filter(province=r_dict['province']).first()
        c_obj = Cities.objects.filter(city=r_dict['city']).first()

        Persons.objects.create(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic=e_obj, birthday=r_dict['birthday'], province=p_obj, city=c_obj, address=r_dict['address'])

        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 删除person
def delete_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        # print('delete从前端发送来的数据：', r_dict, r_dict['id'])

        Persons.objects.filter(id=r_dict['id']).delete()

        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 修改person
def update_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print('update从前端发送来的数据：', r_dict, r_dict['id'])

        e_obj = Ethnics.objects.filter(ethnic=r_dict['ethnic']).first()
        p_obj = Provinces.objects.filter(province=r_dict['province']).first()
        c_obj = Cities.objects.filter(city=r_dict['city']).first()

        Persons.objects.filter(id=r_dict['id']).update(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic=e_obj, birthday=r_dict['birthday'], province=p_obj, city=c_obj, address=r_dict['address'])

        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 搜索person
def search_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print('search从前端发送来的数据：', r_dict)

        user_qs = Persons.objects.all().values()

        for key in r_dict:
            print(key, r_dict[key])
            if r_dict[key] is not None:
                if key == 'number':
                    user_qs = user_qs.filter(number=r_dict[key]).values()
                    print(user_qs)
                    continue
                if key == 'name':
                    user_qs = user_qs.filter(name=r_dict[key]).values()
                    print(user_qs)
                    continue
                if key == 'sex':
                    user_qs = user_qs.filter(sex=r_dict[key]).values()
                    print(user_qs)
                    continue
                if key == 'ethnic':
                    e_obj = Ethnics.objects.filter(ethnic=r_dict['ethnic']).first()  # 获取对象，用于查询
                    user_qs = user_qs.filter(ethnic=e_obj).values()  #
                    print(user_qs)
                    continue
                if key == 'birthday':
                    user_qs = user_qs.filter(birthday=r_dict[key]).values()
                    print(user_qs)
                    continue
                if key == 'province':
                    p_obj = Provinces.objects.filter(province=r_dict['province']).first()
                    user_qs = user_qs.filter(province=p_obj).values()  #
                    print(user_qs)
                    continue
                if key == 'city':
                    c_obj = Cities.objects.filter(city=r_dict['city']).first()
                    user_qs = user_qs.filter(city=c_obj).values()  #
                    print(user_qs)
                    continue
        print('筛选后：', user_qs)

        u = user_qs  # 后面替换的过程直接复制Persons里面的，所以定义一个u，不过这里的u并不是列表[]
        # 替换掉三个_id字段
        for i in range(0, len(u)):
            print(u[i], u[i]['ethnic_id'], u[i]['province_id'], u[i]['city_id'])
            e_obj = Ethnics.objects.filter(id=u[i]['ethnic_id']).values()
            p_obj = Provinces.objects.filter(id=u[i]['province_id']).values()
            c_obj = Cities.objects.filter(id=u[i]['city_id']).values()
            print(e_obj[0]['ethnic'], p_obj[0]['province'], c_obj[0]['city'])

            del u[i]['ethnic_id']  # 删除字段
            del u[i]['province_id']
            del u[i]['city_id']
            u[i]['ethnic'] = e_obj[0]['ethnic']  # 添加字段
            u[i]['province'] = p_obj[0]['province']
            u[i]['city'] = c_obj[0]['city']
            print(u[i])  # 将三个_id字段替换是为了与前端表格中的字段对应，方便展示。结果如下：
            # {
            #  'id': 6,
            #  'number': '2435',
            #  'name': '肥肉',
            #  'sex': 1,
            #  'birthday': datetime.date(2023, 7, 11),
            #  'address': '王斐然',
            #  'ethnic': '回族',
            #  'province': '内蒙古自治区',
            #  'city': '通辽市'
            # }
        print('( user_qs == u ) ==', u==user_qs)
        # 二者全等，下面用哪个都一样
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 发送所有省份provinces
def get_provinces(request):
    if request.method == "GET":
        p = Provinces.objects.all().values()
        resp_data = {'items': list(p)}
        # print(resp_data)
        return JsonResponse(resp_data)


# 发送所有城市cities
def get_cities(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        print('city从前端发送来的数据：', r_dict)  # {'province', 省份}

        p = Provinces.objects.filter(province=r_dict['province']).first()
        c = p.cities_set.all().values()  # 一对多反向查询
        print(c)
        resp_data = {'items': list(c)}
        # print(resp_data)
        return JsonResponse(resp_data)


# 发送所有民族ethnics
def get_ethnics(request):
    if request.method == "GET":
        e = Ethnics.objects.all().values()
        resp_data = {'items': list(e)}
        # print(resp_data)
        return JsonResponse(resp_data)



