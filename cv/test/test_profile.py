from django.test import TestCase, Client
from jobseeker.models import CV, Users
from django.urls import reverse
from django.http import HttpResponse


class ProfileTestCase(TestCase):
    
    def setUp(self):
        self.CV_PROFILE = "cv:profile"

        created_user = Users.objects.create(
            username="username",
            password="password",
            email="emailku@mail.com",
            image="default.png",
            npm=1,
            prodi_id=1,
            role_id=1
        )
        CV.objects.create(
            users_id=created_user,
            profile="profile",
            posisi = "manager",
            instansi = "PT. CBA",
            lama_instansi = "1 tahun",
            keterangan_posisi = "mengurus jalannya PT. CBA",
            asal_sekolah = "SMA Negeri 429",
            masa_waktu = "2010-2013",
            keterangan_pendidikan = "Sarjana",
            kontak = "08123456789",
            jenis_kontak = "WA",
            kemampuan = "menguasai bahasa inggris",
            prestasi = "Juara 1 lomba menulis",
        )

    def test_profile_if_user_is_logged_in(self):
        
        client = Client()
        client.login(username="username",password="password")
        url = reverse(self.CV_PROFILE)
        response = client.get(url)
        self.assertEquals(response.status_code , 200)

    def test_profile_if_user_is_not_logged_in_should_redirect_to_login(self):
        client = Client()
        url = reverse(self.CV_PROFILE)
        response = client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_profile_on_render_should_return_CV(self):
        client = Client()
        client.login(username="username",password="password")
        url = reverse(self.CV_PROFILE)
        response = client.get(url)
        self.assertEquals(response.context['cv'].profile, "profile")

    def test_profile_should_render_profile_template(self):
        client = Client()

        client.login(username="username",password="password")
        url = reverse(self.CV_PROFILE)
        response = client.get(url)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_should_return_http_response(self):
        client = Client()
        client.login(username="username",password="password")
        url = reverse(self.CV_PROFILE)
        response = client.get(url)
        self.assertIsInstance(response, HttpResponse)



