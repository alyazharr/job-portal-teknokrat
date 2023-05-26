from django.test import TestCase
from django.test import Client
from ..models import Users, Lowongan,Lamar
from datetime import datetime, timedelta
from django.urls import reverse
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages import get_messages

LOGIN = 'homepage:login'
MSG_NO_AKSES = 'Anda tidak memiliki akses.'

class BukaLowonganViews(TestCase):
    
    def setUp(self):
        self.alumni = Users.objects.create (
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )

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
                "requirements" : "asda",
                "buka_lowongan" : timezone.now().date(),
                "batas_pengumpulan" : timezone.now().date() + timedelta(days=1)
            }
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
                "buka_lowongan" : timezone.now().date(),
                "batas_pengumpulan" : timezone.now().date() + timedelta(days=1)
            },
        )
        
        assert buka_lowongan_response.status_code == 403 

class EditLowonganViews(TestCase):
    
    def setUp(self):
        self.alumni = Users.objects.create (
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )

        self.perusahaan = Users.objects.create (
            username="perusahaan",
            password="password",
            npm=2,
            prodi_id=2,
            role_id=2
        )

        self.perusahaan2 = Users.objects.create (
            username="perusahaan2",
            password="password",
            npm=3,
            prodi_id=3,
            role_id=2
        )

        self.lowongan =  Lowongan.objects.create(
            users_id=self.perusahaan,
            posisi="Junior Software engineer",
            status="Belum terverifikasi",
            lama_pengalaman=1,
            gaji=1000,
            buka_lowongan=timezone.now().date(),
            batas_pengumpulan=timezone.now().date() + timedelta(days=1)
        )
      
        self.url = reverse('edit-lowongan', args=[self.lowongan.id])
    
    def test_edit_lowongan_should_render_edit_lowongan_template(self):
        client = Client()
        client.login(username='perusahaan',password='password')
        response = client.get(self.url)
        self.assertTemplateUsed(response, 'buka_lowongan.html')
        
    def test_edit_lowongan_from_perusahaan(self):
        client = Client()
        client.login(username='perusahaan',password='password')
        edit_lowongan_response = client.post(
            self.url,
            {
                "posisi" : "Senior Software Engineer",
                "gaji" : 5000,
                "lama_pengalaman" : 5,
                "deskripsi" : "Backend Developer",
                "requirements" : json.dumps(["s1"]),
                "buka_lowongan" : timezone.now().date(),
                "batas_pengumpulan" : timezone.now().date() + timedelta(days=1)
            },
        )
        
        assert edit_lowongan_response.status_code == 302
        edited_lowongan = Lowongan.objects.get(users_id__username='perusahaan')
        assert edited_lowongan != None
        assert edited_lowongan.users_id == self.perusahaan 
        assert edited_lowongan.lama_pengalaman == 5

    def test_edit_lowongan_from_another_perusahaan(self):
        client = Client()
        client.login(username='perusahaan2',password='password')
        edit_lowongan_response = client.post(
            self.url,
            {
                "posisi" : "Senior Software Engineer",
                "gaji" : 5000,
                "lama_pengalaman" : 5,
                "deskripsi" : "Backend Developer",
                "requirements" : json.dumps(["s1"]),
                "buka_lowongan" : timezone.now().date(),
                "batas_pengumpulan" : timezone.now().date() + timedelta(days=1)
            },
        )
        
        assert edit_lowongan_response.status_code == 302
    
    def test_edit_lowongan_from_alumni(self):
        client = Client()
        client.login(username='alumni',password='password')
        edit_lowongan_response = client.post(
            self.url,
            {
                "posisi" : "Senior Software Engineer",
                "gaji" : 5000,
                "lama_pengalaman" : 5,
                "deskripsi" : "Backend Developer",
                "requirements" : json.dumps(["s1"]),
                "buka_lowongan" : datetime.today().strftime("%m/%d/%Y"),
                "batas_pengumpulan" : (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")
            },
        )
        
        assert edit_lowongan_response.status_code == 302

class ListLowonganViewTestCase(TestCase):

    def setUp(self):
        self.alumni = Users.objects.create (
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )

        self.perusahaan = Users.objects.create (
            username="perusahaan",
            password="password",
            npm=2,
            prodi_id=2,
            role_id=2
        )

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

class DetailLowonganTestCase(TestCase):

    def setUp(self):

        self.alumni = Users.objects.create (
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )

        self.perusahaan = Users.objects.create (
            username="perusahaan",
            password="password",
            npm=2,
            prodi_id=2,
            role_id=2
        )

        self.admin = Users.objects.create (
            username="adminsuper",
            password="adminsuper",
            npm=2,
            prodi_id=4,
            role_id=4
        )

        self.lowongan = Lowongan.objects.create(
                users_id=self.perusahaan,
                posisi="Software engineer",
                status="Buka",
                lama_pengalaman=10,
                gaji=100,
                buka_lowongan=timezone.now().date(),
                batas_pengumpulan=timezone.now().date() + timedelta(days=1),
            )


        self.url = f'detail_lowongan'
        self.client = Client()

    def test_unauthenticated_user_should_redirect_to_login(self):
        response = self.client.get(reverse(self.url,args=[ self.lowongan.id ]))
        self.assertEqual(response.status_code, 302)

    def test_lamar_object_should_not_be_created_if_lowongan_not_open(self):
        closed_lowongan = Lowongan.objects.create(
                users_id=self.perusahaan,
                posisi="Software engineer",
                status="Tutup",
                lama_pengalaman=10,
                gaji=100,
                buka_lowongan=timezone.now().date(),
                batas_pengumpulan=timezone.now().date() + timedelta(days=1),    
        )
        self.client.login(username='alumni',password='password')
        response = self.client.post(
            reverse(self.url,args=[ closed_lowongan.id ]),
            {
                "users_id" : self.alumni.id,
                "lowongan_id" : closed_lowongan.id
            }
        )
         
        self.assertRaises(ObjectDoesNotExist, Lamar.objects.get,users_id=self.alumni.id,lowongan_id=closed_lowongan.id)

    def test_lamar_object_should_be_created_if_user_lamar_is_alumni(self):
        self.client.login(username='alumni',password='password')
        response = self.client.post(
            reverse(self.url,args=[ self.lowongan.id ]),
            {
                "users_id" : self.alumni.id,
                "lowongan_id" : self.lowongan.id
            }
        )
        created_lamar = Lamar.objects.get(users_id=self.alumni.id,lowongan_id=self.lowongan.id)
        self.assertIsNotNone(created_lamar)

    def test_lamar_object_should_be_created_if_user_lamar_is_perusahaan(self):
        self.client.login(username='perusahaan',password='password')
        response = self.client.post(
            reverse(self.url,args=[ self.lowongan.id ]),
            {
                "users_id" : self.perusahaan.id,
                "lowongan_id" : self.lowongan.id
            }
        )
        self.assertRedirects(response, reverse(LOGIN)) 
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), MSG_NO_AKSES)

    def test_lamar_object_should_be_created_if_user_lamar_is_admin(self):
        self.client.login(username='adminsuper',password='adminsuper')
        response = self.client.post(
            reverse(self.url,args=[ self.lowongan.id ]),
            {
                "users_id" : self.admin.id,
                "lowongan_id" : self.lowongan.id
            }
        )
        self.assertRedirects(response, reverse(LOGIN)) 
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), MSG_NO_AKSES)

    def test_lamar_object_should_only_be_created_once_if_user_already_lamar(self):
        self.client.login(username='alumni',password='password')
        self.client.post(
            reverse(self.url,args=[ self.lowongan.id ]),
            {
                "users_id" : self.alumni.id,
                "lowongan_id" : self.lowongan.id
            }
        )
        self.client.post(
            reverse(self.url,args=[ self.lowongan.id ]),
            {
                "users_id" : self.alumni.id,
                "lowongan_id" : self.lowongan.id
            }
        )
        total_created_lamar =  Lamar.objects.filter(users_id=self.alumni.id, lowongan_id=self.lowongan.id).count()
        self.assertEqual(total_created_lamar,1)

    
    def test_detail_lowongan_should_return_detail_lowongan_template(self):
        self.client.login(username='alumni',password='password')
        response = self.client.get(reverse(self.url,args=[ self.lowongan.id ]))
        self.assertTemplateUsed(response, 'detail_lowongan.html')
    
    def test_detail_lowongan_should_return_404_if_lowongan_does_not_exist(self):
        self.client.login(username='alumni',password='password')
        response = self.client.get(reverse(self.url,args=[ 34345678 ]))
        self.assertEqual(response.status_code, 404)

    def test_detail_lowongan_should_return_lowongan_by_pk(self):
        self.client.login(username='alumni',password='password')
        response = self.client.get(reverse(self.url,args=[ self.lowongan.id ]))
        detail_lowongan = response.context['detail_lowongan']
        self.assertEqual(self.lowongan, detail_lowongan)
