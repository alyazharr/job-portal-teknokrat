from django.views.generic.edit import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import BukaLowonganForm

class BukaLowonganFormView(UserPassesTestMixin,FormView):
    template_name = 'buka_lowongan.html'
    form_class = BukaLowonganForm
    success_url = '/admin/jobseeker/lowongan'
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role_id == 2

    def form_valid(self, form):
        form.instance.users_id = self.request.user
        form.save()
        return super().form_valid(form)