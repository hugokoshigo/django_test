# coding:utf-8
from django.shortcuts import redirect, reverse
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from app.utils.permission import dashboard_auth
from libs.base_render import render_to_response
from django.core.paginator import Paginator


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("dashboard_index"))
        to = request.GET.get('to', '')
        data = {"error": "", "to": to}
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        to = request.GET.get('to', '')
        data = {"error": ""}
        exist = User.objects.filter(username=username).exists()

        if not exist:
            data["error"] = "用户不存在"
            return render_to_response(request, self.TEMPLATE, data=data)
        user = authenticate(username=username, password=password)

        if not user:
            data["error"] = "密码错误"
            return render_to_response(request, self.TEMPLATE, data=data)

        if not user.is_superuser:
            data["error"] = "无权登录"
            return render_to_response(request, self.TEMPLATE, data=data)

        login(request, user)
        if to:
            return redirect(to)
        return redirect(reverse("dashboard_index"))


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(reverse("dashboard_login"))


class AdminManager(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        users = User.objects.all()
        # 分页
        page = int(request.GET.get('page', 1))
        p = Paginator(users, 2)
        total_page = p.num_pages
        if page <= 1:
            page = 1
        current_page = p.get_page(page).object_list
        data = {'users': current_page, 'total': total_page, 'page_num': page}
        print(data)
        return render_to_response(request, self.TEMPLATE, data=data)


class UpdateAdminStatus(View):

    def get(self, request):
        status = request.GET.get('status', 'on')
        _status = True if status == 'on' else False
        print(request.user.is_superuser,_status)
        # request.user.is_superuser = _status
        # request.user.save()
        return redirect(reverse("dashboard_admin"))
