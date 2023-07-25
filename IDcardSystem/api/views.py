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
        # print(u, len(u))
        resp_data = {'items': u}
        return JsonResponse(resp_data)


# 添加person
def add_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)  # 前端向后端发送的参数
        # print('add从前端发送来的数据：', r_dict, r_dict['number'])

        Persons.objects.create(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic=r_dict['ethnic'], birthday=r_dict['birthday'], province=r_dict['province'], city=r_dict['city'], address=r_dict['address'])

        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 删除person
def delete_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        # print('delete从前端发送来的数据：', r_dict, r_dict['id'])

        Persons.objects.filter(id=r_dict['id'], number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic=r_dict['ethnic'], birthday=r_dict['birthday'], province=r_dict['province'], city=r_dict['city'], address=r_dict['address']).delete()

        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 修改person
def update_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        # print('update从前端发送来的数据：', r_dict, r_dict['id'])

        Persons.objects.filter(id=r_dict['id']).update(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic=r_dict['ethnic'], birthday=r_dict['birthday'], province=r_dict['province'], city=r_dict['city'], address=r_dict['address'])

        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 搜索person
def search_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        # print('search从前端发送来的数据：', r_dict)

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
                    user_qs = user_qs.filter(ethnic=r_dict[key]).values()
                    print(user_qs)
                    continue
                if key == 'birthday':
                    user_qs = user_qs.filter(birthday=r_dict[key]).values()
                    print(user_qs)
                    continue
                if key == 'province':
                    user_qs = user_qs.filter(province=r_dict[key]).values()
                    print(user_qs)
                    continue
                if key == 'city':
                    user_qs = user_qs.filter(city=r_dict[key]).values()
                    print(user_qs)
                    continue
        print(user_qs)
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 发送所有省份provinces
def provinces(request):
    if request.method == "GET":
        p = Provinces.objects.all().values()
        resp_data = {'items': list(p)}
        # print(resp_data)
        return JsonResponse(resp_data)


# 发送所有城市cities
def cities(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        # print('city从前端发送来的数据：', r_dict)

        p = Provinces.objects.filter(province=r_dict['province']).values()
        # print(p, p[0]['id'])
        p_id=p[0]['id']
        c = Cities.objects.filter(province_id=p_id).values()
        # print(c)
        resp_data = {'items': list(c)}
        # print(resp_data)
        return JsonResponse(resp_data)


# 发送所有民族ethnics
def ethnics(request):
    if request.method == "GET":
        e = Ethnics.objects.all().values()
        resp_data = {'items': list(e)}
        # print(resp_data)
        return JsonResponse(resp_data)



