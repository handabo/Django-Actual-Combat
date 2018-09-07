from django.conf.urls import url

from app import views

urlpatterns = [
    # 首页
    url(r'^home/', views.home, name='home'),

    # 闪购
    url(r'^market/', views.market, name='market'),
    url(r'^marketparams/(\d+)/(\d+)/(\d+)/', views.marketparams, name='marketparams'),

    # 购物车主页
    url(r'^cart/', views.cart, name='cart'),
    # 添加商品
    url(r'^addCart/', views.addcart, name='addcart'),
    url(r'^subCart/', views.subcart, name='subcart'),


    # 我的
    url(r'^mine/', views.mine, name='mine'),
]
