import unittest
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponse
from jobseeker.models import Users, CV
from django.db import IntegrityError

class ResumeTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp() 
        self.CV_PROFILE = "cv:profile"
        self.CV_RESUME = "cv:resume"

        try:
            self.created_user_1 = Users.objects.create(
                username="pengguna1",
                password="password",
                email="emailku@mail.com",
                image="default.png",
                npm=1,
                prodi_id=1,
                role_id=1
            )
        except IntegrityError:
            self.created_user_1 = Users.objects.get(username="pengguna1")

        try: 
            self.created_user_2 = Users.objects.create(
                username="penjahat",
                password="password2",
                email="emailku2@mail.com",
                image="default.png",
                npm=2,
                prodi_id=1,
                role_id=1
            )

        except IntegrityError:
            self.created_user_2 = Users.objects.get(username="penjahat")

        self.cv_1 = CV.objects.create(
            users_id=self.created_user_1,
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
    

        self.cv_2 = CV.objects.create(
            users_id=self.created_user_2,
            profile="profile2",
            posisi = "manager2",
            instansi = "PT. CBA2",
            lama_instansi = "5 tahun",
            keterangan_posisi = "mengurus jalannya PT. CBA2",
            asal_sekolah = "SMA Negeri 4292",
            masa_waktu = "2010-2023",
            keterangan_pendidikan = "Magister",
            kontak = "55555555555",
            jenis_kontak = "WA",
            kemampuan = "menguasai bahasa spanyol",
            prestasi = "Juara",
        )
        
    
    def test_resume_if_user_is_logged_in(self):
        client = Client()
        client.login(username="pengguna1",password="password")
        url = reverse(self.CV_RESUME, kwargs={"username":"pengguna1"})
        response = client.get(url)
        self.assertEquals(response.status_code , 200)

    def test_resume_if_user_is_not_logged_in_should_redirect_to_login(self):
        client = Client()
        url = reverse(self.CV_RESUME, kwargs={"username":"pengguna1"})
        response = client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_resume_on_render_should_return_CV(self):
        client = Client()
        client.login(username="pengguna1",password="password")
        url = reverse(self.CV_RESUME, kwargs={"username":"penjahat"})
        response = client.get(url)
        self.assertEquals(response.context['cv'].users_id.username, "penjahat")
    
    def test_resume_on_render_should_return_other_user(self):
        client = Client()
        client.login(username="pengguna1",password="password")
        url = reverse(self.CV_RESUME, kwargs={"username":"penjahat"})
        response = client.get(url)
        self.assertEquals(response.context['user'].username, "penjahat")

    def test_resume_on_render_should_return_message(self):
        client = Client()
        client.login(username="pengguna1",password="password")
        url = reverse(self.CV_RESUME, kwargs={"username":"pengguna3"})
        response = client.get(url)
        self.assertEquals(response.context['message'], "User tidak ditemukan.")