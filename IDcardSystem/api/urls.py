from django.urls import path
from . import views


urlpatterns = [
    # ========== 函数视图 ==========
    path('login/', views.login),
    # path('register/', views.register),
    path('get_code/', views.get_code),
    path('get_persons/', views.get_persons),
    path('add_person/', views.add_person),
    path('delete_person/', views.delete_person),
    path('update_person/', views.update_person),
    path('get_provinces/', views.get_provinces),
    path('get_cities/', views.get_cities),
    path('get_ethnics/', views.get_ethnics),

    # ========== 类视图 ==========
    path('persons/', views.PersonsView.as_view()),  # as_view() 类视图使用规范，必带
    path('persons/<int:pk>/', views.PersonsView.as_view()),  # <...> 相当于占位符，用于在url上展示参数。其中可限制参数的数据类型和名称
    path('register/', views.RegisterView.as_view()),
    path('redis_test/', views.RedisTestView.as_view())
]
