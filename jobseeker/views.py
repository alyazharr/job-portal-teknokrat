from django.views.generic.edit import FormView, FormMixin, UpdateView
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import BukaLowonganForm,LamarForm
from .models import Lowongan, Lamar
from django.db.models import Q

LOGINURL = '/login/'

class BukaLowonganFormView(UserPassesTestMixin,FormView):
    template_name = 'buka_lowongan.html'
    form_class = BukaLowonganForm
    success_url = '/dashboard-lowongan-pekerjaan/'
    login_url = LOGINURL

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role_id == 2

    def form_valid(self, form):
        form.instance.users_id = self.request.user
        form.save()
        return super().form_valid(form)
    
class EditLowonganFormView(UserPassesTestMixin,UpdateView):
    template_name = 'buka_lowongan.html'
    model = Lowongan
    form_class = BukaLowonganForm
    success_url = '/dashboard-lowongan-pekerjaan/'
    login_url = LOGINURL

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role_id == 2

class ListLowonganView(UserPassesTestMixin, ListView):
    model = Lowongan
    context_object_name = 'list_lowongan'
    template_name = 'list_lowongan.html'
    paginate_by = 10
    login_url = LOGINURL
    ordering = ('-batas_pengumpulan',)

    def test_func(self):
        return self.request.user.is_authenticated 

    def get_queryset(self):
        if self.request.GET.get('search_query',""):
            return super().get_queryset().search(self.request.GET['search_query'])
        
        return super().get_queryset().all_open_lowongan()

class DetailLowonganView(FormMixin,UserPassesTestMixin,DetailView):
    model = Lowongan
    form_class = LamarForm
    template_name = 'detail_lowongan.html'
    context_object_name = 'detail_lowongan'
    login_url = LOGINURL
    success_url = '/list_lowongan/'

    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def lamaran_is_valid(self):
        # check jika pengguna telah melamar
        lowongan = Lowongan.objects.get(id=self.kwargs.get('pk'))
        already_lamar = Lamar.objects.filter(users_id=self.request.user.id,lowongan_id=self.kwargs.get('pk')).exists()
        return not already_lamar and lowongan.is_open

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid() and self.lamaran_is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
       
    def get_context_data(self, **kwargs):
        already_lamar = Lamar.objects.filter(users_id=self.request.user.id,lowongan_id=self.kwargs.get('pk')).exists()
        if already_lamar:
            kwargs['already_lamar'] = True
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.is_authenticated

