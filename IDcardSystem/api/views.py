from django.http import JsonResponse
from api.models import Persons, Provinces, Cities, Ethnics
import json


# 发送persons
def get_persons(request):
    if request.method == "GET":
        page_size = int(request.GET.get('pageSize'))  # str转int，当前页显示条数
        current_page = int(request.GET.get('currentPage'))  # 当前是第几页
        query_fields = ('number', 'name', 'sex', 'ethnic__name', 'birthday', 'city__province__name', 'city__name')
        query_params = {}
        for i in query_fields:
            if request.GET.get(i):
                query_params[i] = request.GET.get(i)
        # print('query_params', query_params)
        persons_qs = Persons.objects.filter(**query_params)  # 不定传参，*列表，**字典
        # print('persons_qs', persons_qs)
        total = persons_qs.count()  # 获取数据总条数
        persons_qs = persons_qs[(current_page - 1)*page_size:current_page*page_size].values()
        # 例 Persons.objects.all()[0:5] 表示直接拿到第1到第5条person数据
        # print('persons_qs', persons_qs)
        for person in persons_qs:
            ethnic__name = Ethnics.objects.filter(id=person['ethnic_id']).values()[0]['name']  # 民族name
            city_obj = Cities.objects.filter(id=person['city_id'])
            city__name = city_obj.values()[0]['name']  # 城市name
            city__province__name = city_obj.values('province__name')[0]['province__name']  # 省份name
            # print(ethnic__name, city__name, city__province__name)
            del person['ethnic_id']
            del person['city_id']
            person['ethnic__name'] = ethnic__name
            person['city__name'] = city__name
            person['city__province__name'] = city__province__name
        # print(persons_qs)

        # 注意：__跨表不仅能在filter里面使用，还可以在values里面用。
        # （1）Persons.objects.filter(city__name='北京市').values()  # 查询 北京市 包含的person（已知城市，查人）
        # print(Persons.objects.filter(name='张三').values('city__name'))  # 验证√
        # （2）Persons.objects.filter(name='张三').values('city__name')  # 查询 张三 所属城市的name（已知人，查城市）
        # print(Persons.objects.filter(city__name='北京市').values())  # 验证√

        resp_data = {'items': list(persons_qs), 'total': total}
        return JsonResponse(resp_data)


# 添加person
def add_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)  # 前端向后端发送的参数
        ethnic_obj = Ethnics.objects.filter(name=r_dict['ethnic__name']).first()  # 先获取对象，后创建
        city_obj = Cities.objects.filter(name=r_dict['city__name']).first()
        Persons.objects.create(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic=ethnic_obj, birthday=r_dict['birthday'], city=city_obj, address=r_dict['address'])

        # 注意：__跨表不能用在create和update里面，只能在跨表查询的时候用。
        # （1）Persons.objects.create(number=r_dict['number'], name=r_dict['name'],sex=r_dict['sex'], ethnic__name=r_dict['ethnic'], birthday=r_dict['birthday'], city__name=r_dict['city'], address=r_dict['address'])  # 验证×
        # （2）Persons.objects.filter(id=r_dict['id']).update(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic__name=r_dict['ethnic'], birthday=r_dict['birthday'], city__name=r_dict['city'], address=r_dict['address'])  # 验证×

        # 后面这些实际用不到，只是想给前端一个反馈
        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 删除person
def delete_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        Persons.objects.filter(id=r_dict['id']).delete()

        # 后面这些实际用不到，只是想给前端一个反馈
        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
        return JsonResponse(resp_data)


# 修改person
def update_person(request):
    if request.method == "POST":
        r_dict = json.loads(request.body)
        ethnic_obj = Ethnics.objects.filter(name=r_dict['ethnic__name']).first()
        city_obj = Cities.objects.filter(name=r_dict['city__name']).first()
        Persons.objects.filter(id=r_dict['id']).update(number=r_dict['number'], name=r_dict['name'], sex=r_dict['sex'], ethnic=ethnic_obj, birthday=r_dict['birthday'], city=city_obj, address=r_dict['address'])

        # 后面这些实际用不到，只是想给前端一个反馈
        user_qs = Persons.objects.all().values()
        resp_data = {'items': list(user_qs)}
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



