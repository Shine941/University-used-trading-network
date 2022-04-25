from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class LoginRequiredJSONMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'code':400,'errmsg':'没有登录'})
        return super().dispatch(request, *args, **kwargs)