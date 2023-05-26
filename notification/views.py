from jobseeker.models import Users
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from jobseeker.models import Users

class SubscriptionView(UserPassesTestMixin, View):
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role_id == 1

    def get(self,request, *args, **kwargs):
        user = Users.objects.get(id=request.user.id)
        user.subscribed = not user.subscribed
        user.save()

        try:
            return redirect(request.META.get('HTTP_REFERER'))    
        except:
            return redirect('homepage:home')
