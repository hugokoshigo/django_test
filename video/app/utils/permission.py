# coding:utf-8

import functools

from django.shortcuts import redirect, reverse


def dashboard_auth(func):
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwagrs):
        user = request.user
        if not user.is_authenticated or not user.is_superuser:
            return redirect('{}?to={}'.format(reverse("dashboard_login"), request.path))
        return func(self, request, *args, **kwagrs)

    return wrapper
