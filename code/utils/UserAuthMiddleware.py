
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import reverse

from user.models import UserTicketModel, UserModel


class UserMiddle(MiddlewareMixin):

    def process_request(self, request):

        # 需要登录验证，个人中心和购物车和商品的增删
        need_login = ['/axf/mine/']
        if request.path in need_login:
            # 先获取cookies中的ticket参数
            ticket = request.COOKIES.get('ticket')
            # 如果没有ticket，则直接跳转到登录
            if not ticket:
                return HttpResponseRedirect(reverse('user:login'))

            user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
            if user_ticket:
                # 获取到有认证的相关信息
                # 1. 验证当前认证信息是否过期，如果没过期，request.user赋值
                # 2. 如果过期了，跳转到登录，并删除认证信息
                if datetime.utcnow() > user_ticket.out_time.replace(tzinfo=None):
                    # 过期
                    UserTicketModel.objects.filter(user=user_ticket.user).delete()
                    return HttpResponseRedirect(reverse('user:login'))
                else:
                    # 没有过期，赋值request.user，并且删除多余的认证信息
                    request.user = user_ticket.user
                    # 删除多余的认证信息，
                    # 从UserTicket中查询当前user，并且ticket不等于cookie中的ticket
                    UserTicketModel.objects.filter(Q(user=user_ticket.user) &
                                                   ~Q(ticket=ticket)).delete()
                    return None
            else:
                return HttpResponseRedirect(reverse('user:login'))
        else:
            return None
