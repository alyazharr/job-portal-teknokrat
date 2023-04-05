from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import BukaLowonganForm
from .models import Lowongan
from django.db.models import Q

class BukaLowonganFormView(UserPassesTestMixin,FormView):
    template_name = 'buka_lowongan.html'
    form_class = BukaLowonganForm
    success_url = '/list_lowongan'
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role_id == 2

    def form_valid(self, form):
        form.instance.users_id = self.request.user
        form.save()
        return super().form_valid(form)

class ListLowonganView(UserPassesTestMixin, ListView):
    model = Lowongan
    context_object_name = 'list_lowongan'
    template_name = 'list_lowongan.html'
    paginate_by = 10
    login_url = '/login/'
    ordering = ('-batas_pengumpulan',)

    def test_func(self):
        return self.request.user.is_authenticated 

    def get_queryset(self):
        if 'search_query' in self.request.GET and self.request.GET['search_query'] != "":
            self.queryset = Lowongan.objects.filter(
                (
                    Q(posisi__icontains=self.request.GET['search_query']) |
                    Q(users_id__name__icontains=self.request.GET['search_query'])
                )
            )
        else:
            self.queryset = Lowongan.objects.all()

        return super().get_queryset()