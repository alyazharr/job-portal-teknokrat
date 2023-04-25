import unittest
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponse
from jobseeker.models import Users, CV
from django.db import IntegrityError

class EditResumeTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp() 
        self.CV_PROFILE = "cv:profile"
        self.CV_RESUME_EDIT = "cv:edit-resume"

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
        
    def test_edit_resume_should_return_200_when_logged_in(self):
        client = Client()
        client.login(username="pengguna1", password="password")
        response = client.get(reverse(self.CV_RESUME_EDIT))
        self.assertEqual(response.status_code, 200)

    def test_edit_resume_should_return_302_when_not_logged_in(self):
        client = Client()
        response = client.get(reverse(self.CV_RESUME_EDIT))
        self.assertEqual(response.status_code, 302)

    def test_edit_resume_should_return_302_when_success_edit(self):
        client = Client()
        client.login(username="pengguna1", password="password")
        response = client.post(reverse(self.CV_RESUME_EDIT), {
            'name': 'pengguna1',
            'email': 'emailku@mail.com',
            'no_telp': '08123456789',
            'alamat': 'Jl. Jalan',
            'tempat_lahir': 'Jakarta',
            'tgl_lahir': '1999-01-01',
            'ipk': '3.5',
            'profile': 'profile',
            'posisi': 'manager',
            'instansi': 'PT. CBA',
            'lama_instansi': '1 tahun',
            'keterangan_posisi': 'mengurus jalannya PT. CBA',
            'asal_sekolah': 'SMA Negeri 429',
            'masa_waktu': '2010-2013',
            'keterangan_pendidikan': 'Sarjana',
            'kontak': '08123456789',
            'jenis_kontak': 'WA',
            'kemampuan': 'menguasai bahasa inggris',
            'prestasi': 'Juara 1 lomba menulis',
        })
        self.assertEqual(response.status_code, 302)
    
    def test_edit_resume_should_return_200_when_fail_edit(self):
        client = Client()
        client.login(username="pengguna1", password="password")
        response = client.post(reverse(self.CV_RESUME_EDIT), {
            'kontak': '08123456789',
        })
        self.assertEqual(response.status_code, 200)