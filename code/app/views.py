from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, CartModel
from user.models import UserTicketModel


def home(request):
    # 首页视图函数
    if request.method == 'GET':
        mainwheels = MainWheel.objects.all()
        mainnavs = MainNav.objects.all()
        mainmustbuys = MainMustBuy.objects.all()
        mainshops = MainShop.objects.all()
        mainshows = MainShow.objects.all()

        data = {
            'title': '首页',
            'mainwheels': mainwheels,
            'mainnavs': mainnavs,
            'mainmustbuys': mainmustbuys,
            'mainshops': mainshops,
            'mainshows': mainshows,
        }
        return render(request, 'home/home.html', data)


def market(request):
    # 闪购视图函数
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('axf:marketparams',
                                            args=('104749', '0', '0')))


def marketparams(request, typeid, cid, sid):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
        if user_ticket:
            user = user_ticket.user
        else:
            user = ''

        foodtypes = FoodType.objects.all()
        # 展示主分类下的子分类商品
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid,
                                         childcid=cid)

        childtypenames = FoodType.objects.filter(typeid=typeid).first().childtypenames
        # [['国产水果',14111], ['进口水果'：13321]]
        childtypenames_list = [i.split(':') for i in childtypenames.split('#')]

        # 综合排序
        if sid == '0':
            pass
        # 销量排序
        elif sid == '1':
            goods = goods.order_by('-productnum')
        # 价格降序
        elif sid == '2':
            goods = goods.order_by('-price')
        # 价格升序
        elif sid == '3':
            goods = goods.order_by('price')

        if user:
            user_cart = CartModel.objects.filter(user=user)
        else:
            user_cart = ''

        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'cid': cid,
            'sid': sid,
            'childtypenames_liat': childtypenames_list,
            'user_cart': user_cart

        }
        # 将内容渲染到页面
        return render(request, 'market/market.html', data)


def cart(request):
    # 购物车视图函数
    return render(request, 'cart/cart.html')


def addcart(request):
    # 添加商品到购物车
    pass


def subcart(request):
    pass


def mine(request):
    # 我的视图函数
    return render(request, 'mine/mine.html')