from django.test import TestCase
from django.test import Client
from ..models import Users, Lowongan
from datetime import datetime, timedelta
from django.urls import reverse
import json
from django.utils import timezone

class BukaLowonganViews(TestCase):
    
    def setUp(self):
        # set up alumni data
        self.alumni = Users.objects.create (
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )

        # set up perusahaan data
        self.perusahaan = Users.objects.create (
            username="perusahaan",
            password="password",
            npm=2,
            prodi_id=2,
            role_id=2
        )

      
        self.url = 'buka_lowongan'
    
    def test_buka_lowongan_should_render_buka_lowongan_template(self):
        client = Client()
        client.login(username='perusahaan',password='password')
        response = client.get(reverse(self.url))
        self.assertTemplateUsed(response, 'buka_lowongan.html')
        
    def test_buka_lowongan_from_perusahaan(self):
        client = Client()
        client.login(username='perusahaan',password='password')
        buka_lowongan_response = client.post(
            reverse(self.url),
            {
                "posisi" : "Software Engineer",
                "gaji" : 10000,
                "lama_pengalaman" : 10,
                "deskripsi" : "Developer react",
                "requirements" : json.dumps(["s1"]),
                "buka_lowongan" : datetime.today().strftime("%m/%d/%Y"),
                "batas_pengumpulan" : (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")
            },
        )
        
        assert buka_lowongan_response.status_code == 302
        created_lowongan = Lowongan.objects.get(users_id__username='perusahaan')
        assert created_lowongan != None
        assert created_lowongan.users_id == self.perusahaan 
    
    def test_buka_lowongan_from_alumni(self):
        client = Client()
        client.login(username='alumni',password='password')
        buka_lowongan_response = client.post(
            reverse(self.url),
            {
                "posisi" : "Software Engineer",
                "gaji" : 10000,
                "lama_pengalaman" : 10,
                "deskripsi" : "Developer react",
                "requirements" : json.dumps(["s1"]),
                "buka_lowongan" : datetime.today().strftime("%m/%d/%Y"),
                "batas_pengumpulan" : (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")
            },
        )
        
        assert buka_lowongan_response.status_code == 403 

class ListLowonganViewTestCase(TestCase):

    def setUp(self):
        # set up alumni data
        self.alumni = Users.objects.create (
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )

        # set up perusahaan data
        self.perusahaan = Users.objects.create (
            username="perusahaan",
            password="password",
            npm=2,
            prodi_id=2,
            role_id=2
        )

          # 15 lowongan yang statusnya buka

        for i in range(1,16):
            Lowongan.objects.create(
                users_id=self.perusahaan,
                posisi="Software engineer",
                status="Buka",
                lama_pengalaman=10,
                gaji=100,
                buka_lowongan=timezone.now().date(),
                batas_pengumpulan=timezone.now().date() + timedelta(days=i)
            )

        # 5 lowongan yang statusnya tutup
        for i in range(1,6):
            Lowongan.objects.create(
                users_id=self.perusahaan,
                posisi="Software engineer",
                status="Tutup",
                lama_pengalaman=10,
                gaji=100,
                buka_lowongan=timezone.now().date(),
                batas_pengumpulan=timezone.now().date() + timedelta(days=i)
        )

        # 5 lowongan yang yang statusnya Belum terverifikasi
        for i in range(1,6):
            Lowongan.objects.create(
                users_id=self.perusahaan,
                posisi="Software engineer",
                status="Belum terverifikasi",
                lama_pengalaman=10,
                gaji=100,
                buka_lowongan=timezone.now().date(),
                batas_pengumpulan=timezone.now().date() + timedelta(days=i)
        )
        # 5 lowongan yang statusnya sudah terverifikasi
        for i in range(1,6):
            Lowongan.objects.create(
                users_id=self.perusahaan,
                posisi="Software engineer",
                status="Sudah terverifikasi",
                lama_pengalaman=10,
                gaji=100,
                buka_lowongan=timezone.now().date(),
                batas_pengumpulan=timezone.now().date() + timedelta(days=i)
        )
        # 5 lowongan yang statusnya ditolak
        for i in range(1,6):
            Lowongan.objects.create(
                users_id=self.perusahaan,
                posisi="Software engineer",
                status="Ditolak",
                lama_pengalaman=10,
                gaji=100,
                buka_lowongan=timezone.now().date(),
                batas_pengumpulan=timezone.now().date() + timedelta(days=i)
        )



        self.url = 'list_lowongan'  
        self.client = Client()  

    def test_list_lowongan_should_return_list_lowongan_template(self):
        self.client.login(username='alumni',password='password')
        response = self.client.get(reverse(self.url))
        self.assertTemplateUsed(response, 'list_lowongan.html')

    def test_access_if_user_is_not_logged_in_should_redirect_to_login(self):
        response = self.client.get(reverse(self.url))
        assert response.status_code == 302


    def test_list_lowongan_should_return_sorted_by_batas_pengumpulan(self):
        self.client.login(username='alumni',password='password')
        response = self.client.get(reverse(self.url))
        context = response.context

        list_lowongan = context['list_lowongan']
        sorted_list_lowongan = sorted(list_lowongan,key=lambda x : x.batas_pengumpulan,reverse=True)
        self.assertEqual(list(list_lowongan), sorted_list_lowongan)

    def test_list_lowongan_should_be_paginated_ten_items_each(self):
        self.client.login(username='alumni',password='password')
        response = self.client.get(reverse(self.url))
        context = response.context

        list_lowongan = context['list_lowongan']
        self.assertEqual(len(list_lowongan), 10)

    def test_list_lowongan_search_by_query_should_return_correct_item(self):
        search_query = "software engin"
        self.client.login(username='alumni',password='password')
        response = self.client.get(f"{reverse(self.url)}?search_query={search_query}")
        context = response.context
        list_lowongan = context['list_lowongan']

        for lowongan in list_lowongan:
            self.assertEqual(lowongan.posisi, 'Software engineer') 
        
    
    def test_list_lowongan_search_by_nonexisting_lowongan_should_return_empty_list(self):
        search_query = "tidak ada kerja "
        self.client.login(username='alumni',password='password')
        response = self.client.get(f"{reverse(self.url)}?search_query={search_query}")
        context = response.context
        list_lowongan = context['list_lowongan']

        self.assertEqual(len(list_lowongan), 0)

    def test_list_lowongan_should_only_return_with_status_buka(self):
        self.client.login(username='alumni',password='password')
        response = self.client.get(reverse(self.url))
        context = response.context

        list_lowongan = context['list_lowongan']
        
        for lowongan in list_lowongan:
            assert lowongan.status == 'Buka'