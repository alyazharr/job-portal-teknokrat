from django.test import TestCase, Client
from jobseeker.models import Users, Lowongan
from django.urls import reverse
from datetime import datetime, timedelta
import json

global DASHBOARD
DASHBOARD = '/dashboard-lowongan-pekerjaan/'

global LOWONGAN_DIBUKA
LOWONGAN_DIBUKA = '/lowongan-dibuka/'

global LOWONGAN_DITUTUP
LOWONGAN_DITUTUP = '/lowongan-ditutup/'

global LOGIN
LOGIN = 'homepage:login'

global POSISI
POSISI = "Data Scientist"

global DESKRIPSI
DESKRIPSI = "Ahli dalam bidang data dan ML"

global DATE_FORMAT
DATE_FORMAT = "%Y-%m-%d"

class DashboardLowonganNotLoggedIn(TestCase):
    def setUp(self):
        self.url ='/dashboard-lowongan-pekerjaan/'
        PASSWORD_PERUSAHAAN = "Perusahaan123"
        USERNAME_PERUSAHAAN = "iamperusahaan"
        NPM_PERUSAHAAN = 34567890
        PRODI_ID_PERUSAHAAN = 84202
        ROLE_ID_PERUSAHAAN=2

        self.perusahaan = Users.objects.create (
            username=USERNAME_PERUSAHAAN,
            password=PASSWORD_PERUSAHAAN,
            npm=NPM_PERUSAHAAN,
            prodi_id=PRODI_ID_PERUSAHAAN,
            role_id=ROLE_ID_PERUSAHAAN
        )

        self.lowongan = Lowongan.objects.create(
            users_id = self.perusahaan,
            posisi="Data Scientist",
            gaji=8000000,
            lama_pengalaman= 10,
            deskripsi= "Ahli dalam bidang data dan ML",
            requirements=json.dumps(["s1"]),
            buka_lowongan=datetime.today().strftime(DATE_FORMAT),
            batas_pengumpulan=(datetime.today() + timedelta(days=1)).strftime(DATE_FORMAT)
        )
    
    def test_dashboard_response(self):
        client = Client() 
        response = client.get(DASHBOARD) 
        self.assertEquals(response.status_code, 302) 
 
    def test_lowongan_dibuka(self):
        response = Client().get(LOWONGAN_DIBUKA)
        self.assertEqual(response.status_code, 302)

    def test_lowongan_ditutup(self):
        response = Client().get(LOWONGAN_DITUTUP)
        self.assertEqual(response.status_code, 302)

class DashboardLowonganCompany(TestCase):  
    def setUp(self) -> None:
        PASSWORD = "dummy-company"
        USERNAME = "company"
        NAME = "Admin Company"
        NPM = 200767334
        PRODI_ID = 84202

        self.client = Client()
        perusahaan_acc = Users.objects.create(
                username=USERNAME,
                password=PASSWORD,
                name=NAME,
                npm=NPM,
                prodi_id=PRODI_ID,
                role_id=2
            )
        
        PASSWORD_PERUSAHAAN = "Perusahaan123"
        USERNAME_PERUSAHAAN = "iamperusahaan"
        NAME_PERUSAHAAN = "PT PERUSAHAAN"
        NPM_PERUSAHAAN = 34567890
        PRODI_ID_PERUSAHAAN = 84202
        ROLE_ID_PERUSAHAAN=2

        self.perusahaan = Users.objects.create (
            username=USERNAME_PERUSAHAAN,
            password=PASSWORD_PERUSAHAAN,
            name=NAME_PERUSAHAAN,
            npm=NPM_PERUSAHAAN,
            prodi_id=PRODI_ID_PERUSAHAAN,
            role_id=ROLE_ID_PERUSAHAAN
        )

        self.perusahaan2 = Users.objects.create (
            username="perusahaan2",
            password="perusahaan2password",
            name="perusahaan2",
            npm=1234,
            prodi_id=12345,
            role_id=ROLE_ID_PERUSAHAAN
        )

        lowongan1 = Lowongan.objects.create(
            users_id = self.perusahaan,
            posisi=POSISI,
            gaji=8000000,
            lama_pengalaman= 10,
            deskripsi= DESKRIPSI,
            requirements="lorem ipsum 2",
            buka_lowongan=datetime.today().strftime(DATE_FORMAT),
            batas_pengumpulan=(datetime.today() + timedelta(days=1)).strftime(DATE_FORMAT),
            status ='Buka'
        )

        lowongan2 = Lowongan.objects.create(
            users_id = self.perusahaan,
            posisi=POSISI,
            gaji=8000000,
            lama_pengalaman= 10,
            deskripsi= DESKRIPSI,
            requirements="lorem ipsum",
            buka_lowongan=datetime.today().strftime(DATE_FORMAT),
            batas_pengumpulan=(datetime.today() + timedelta(days=1)).strftime(DATE_FORMAT),
            status ='Tutup'
        )

        lowongan_owned_check = Lowongan.objects.create(
            users_id = self.perusahaan2,
            posisi="Sekretaris",
            gaji=1200000,
            lama_pengalaman= 5,
            deskripsi= "bisa bantu saya",
            requirements="bisa atur jadwal saya",
            buka_lowongan=datetime.today().strftime(DATE_FORMAT),
            batas_pengumpulan=(datetime.today() + timedelta(days=1)).strftime(DATE_FORMAT),
            status ='Buka'
        )
        self.lowongan_dibuka = lowongan1
        self.lowongan_dibuka.save()

        self.lowongan_owned = lowongan_owned_check
        self.lowongan_owned.save()

        self.lowongan_ditutup = lowongan2
        self.lowongan_ditutup.save()

        login = self.client.login(username=USERNAME_PERUSAHAAN,password=PASSWORD_PERUSAHAAN)
        self.admin_acc = perusahaan_acc
        self.assertTrue(login)
    
    def test_dashboard_response_logged_in(self):
        response = self.client.get(DASHBOARD)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_lowongan_kerja_perusahaan.html')
        self.assertEqual(response.context['total_lowongan'], 2)
        self.assertEqual(response.context['total_dibuka'], 1)
        self.assertEqual(response.context['total_ditutup'], 1)

    def lowongan_owned_by_perusahaan(self):
        owned_lowongan = Lowongan.objects.get(users_id = self.perusahaan.id)
        self.assertEqual(owned_lowongan[0], self.lowongan_dibuka)

    def lowongan_owned_by_perusahaan2(self):
        owned_lowongan = Lowongan.objects.get(users_id = self.perusahaan2.id)
        self.assertEqual(owned_lowongan, self.lowongan_owned)
        
    def test_lowongan_dibuka_response_logged_in(self):
        response = self.client.get(LOWONGAN_DIBUKA)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lowongan_dibuka.html')
        self.assertContains(response, 'Lowongan Dibuka')

    def test_lowongan_ditutup_response_logged_in(self):
        response = self.client.get(LOWONGAN_DITUTUP)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lowongan_ditutup.html')
        self.assertContains(response, 'Lowongan Ditutup')

    def test_tutup_lowongan(self):
        response = self.client.get(reverse('ubah_status', args=[self.lowongan_dibuka.id]))
        self.assertEqual(response.status_code, 302)
        self.lowongan_dibuka.refresh_from_db()
        self.assertEqual(self.lowongan_dibuka.status, 'Tutup')

class DashboardLowonganTestNotCompany(TestCase):
    def setUp(self) -> None:
        PASSWORD = "NotCompany"
        NAME = "Not Company Dummy"
        USERNAME = "iamnotcompany"
        NPM = 12345678
        PRODI_ID = 84202

        self.client = Client()
        alumni_acc = Users.objects.create(
            username=USERNAME,
            password=PASSWORD,
            name=NAME,
            npm=NPM,
            prodi_id=PRODI_ID,
            role_id=1
        )

        PASSWORD_PERUSAHAAN = "Perusahaan123"
        USERNAME_PERUSAHAAN = "iamperusahaan"
        NPM_PERUSAHAAN = 34567890
        PRODI_ID_PERUSAHAAN = 84202
        ROLE_ID_PERUSAHAAN=2

        self.perusahaan = Users.objects.create (
            username=USERNAME_PERUSAHAAN,
            password=PASSWORD_PERUSAHAAN,
            npm=NPM_PERUSAHAAN,
            prodi_id=PRODI_ID_PERUSAHAAN,
            role_id=ROLE_ID_PERUSAHAAN
        )

        self.lowongan = Lowongan.objects.create(
            users_id = self.perusahaan,
            posisi=POSISI,
            gaji=8000000,
            lama_pengalaman= 10,
            deskripsi= DESKRIPSI,
            requirements=json.dumps(["s1"]),
            buka_lowongan=datetime.today().strftime(DATE_FORMAT),
            batas_pengumpulan=(datetime.today() + timedelta(days=1)).strftime(DATE_FORMAT)
        )
        
        self.alumni_acc = alumni_acc
        login = self.client.login(username=USERNAME,password=PASSWORD)       
        self.assertTrue(login)

    def test_dashboard_response(self):
        response = self.client.get(DASHBOARD)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN))

    def test_lowongan_dibuka_response(self):
        response = self.client.get(LOWONGAN_DIBUKA)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN))
    
    def test_lowongan_ditutup_response(self):
        response = self.client.get(LOWONGAN_DITUTUP)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN))

    def test_ubah_status(self):
        response = self.client.get(reverse('ubah_status', args=[self.lowongan.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN))

    
    
    
       