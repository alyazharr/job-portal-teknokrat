from django.test import TestCase, Client
from jobseeker.models import Users, Lowongan
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import datetime, timedelta
import json

global DASHBOARD
DASHBOARD = '/dashboard-proposal-lowongan/'

global TERVERIFIKASI 
TERVERIFIKASI = '/dashboard-proposal-lowongan/verifikasi'

global RIWAYAT 
RIWAYAT = '/dashboard-proposal-lowongan/riwayat'

global DETAIL 
DETAIL = 'dashboard_proposal_lowongan:detail'

global LOGIN
LOGIN = 'homepage:login'

global POSISI
POSISI = "Data Scientist"

global DESKRIPSI
DESKRIPSI = "Ahli dalam bidang data dan ML"

global DATE_FORMAT
DATE_FORMAT = "%Y-%m-%d"

global MSG_NO_ADMIN
MSG_NO_ADMIN = 'Anda tidak memiliki akses ke laman ini. Silakan login sebagai Admin.'

class BaseTestCase(TestCase):
    PASSWORD_PERUSAHAAN = "Perusahaan123"
    USERNAME_PERUSAHAAN = "iamperusahaan"
    NPM_PERUSAHAAN = 34567890
    PRODI_ID_PERUSAHAAN = 84202
    ROLE_ID_PERUSAHAAN = 2

    def setUp(self) -> None:
        self.perusahaan = Users.objects.create(
            username=self.USERNAME_PERUSAHAAN,
            password=self.PASSWORD_PERUSAHAAN,
            npm=self.NPM_PERUSAHAAN,
            prodi_id=self.PRODI_ID_PERUSAHAAN,
            role_id=self.ROLE_ID_PERUSAHAAN
        )
        self.perusahaan.save()

        self.lowongan = Lowongan.objects.create(
            users_id=self.perusahaan,
            posisi="Data Scientist",
            gaji=8000000,
            lama_pengalaman=10,
            deskripsi="Ahli dalam bidang data dan ML",
            requirements=json.dumps(["s1"]),
            buka_lowongan=datetime.today().strftime(DATE_FORMAT),
            batas_pengumpulan=(datetime.today() + timedelta(days=1)).strftime(DATE_FORMAT)
        )
        self.lowongan.save()

class DashboardProposalLowonganTestNoLogin(BaseTestCase):  
    def test_dashboard_response(self):
        response = Client().get(DASHBOARD)
        self.assertEqual(response.status_code, 302)

    def test_verifikasi_response(self):
        response = Client().get(TERVERIFIKASI)
        self.assertEqual(response.status_code, 302)

    def test_riwayat_response(self):
        response = Client().get(RIWAYAT)
        self.assertEqual(response.status_code, 302)

    def test_detail_page(self):
        url = reverse(DETAIL, args=[self.lowongan.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  

class DashboardProposalLowonganTestNotAdmin(BaseTestCase):
    PASSWORD = "NotAdmin123"
    NAME = "Not Admin Dummy"
    USERNAME = "iamnotadminofteknokrat"
    NPM = 12345678
    PRODI_ID = 84202
    
    def setUp(self) -> None:
        super().setUp()

        self.client = Client()
        alumni_acc = Users.objects.create(
            username=self.USERNAME,
            password=self.PASSWORD,
            name=self.NAME,
            npm=self.NPM,
            prodi_id=self.PRODI_ID,
            role_id=2
        )

        self.alumni_acc = alumni_acc
        login = self.client.login(username=self.USERNAME,password=self.PASSWORD)       
        self.assertTrue(login)
        
    def test_dashboard_response(self):
        response = self.client.get(DASHBOARD)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN)) 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), MSG_NO_ADMIN)

    def test_verifikasi_response(self):
        response = self.client.get(TERVERIFIKASI)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN)) 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), MSG_NO_ADMIN)

    def test_riwayat_response(self):
        response = self.client.get(RIWAYAT)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN)) 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), MSG_NO_ADMIN)

    def test_detail_page(self):
        url = reverse(DETAIL, args=[self.lowongan.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN)) 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Anda tidak memiliki akses ke laman ini. Silakan login sebagai Admin.')

class DashboardProposalLowonganTestAdmin(BaseTestCase):  
    PASSWORD = "dummy-admin"
    USERNAME = "admin-teknokrat"
    NAME = "Admin Dummy"
    NPM = 200767334
    PRODI_ID = 84202

    def setUp(self) -> None:
        super().setUp()

        self.client = Client()
        admin_acc = Users.objects.create(
                username=self.USERNAME,
                password=self.PASSWORD,
                name=self.NAME,
                npm=self.NPM,
                prodi_id=self.PRODI_ID,
                role_id=4
            )

        login = self.client.login(username=self.USERNAME,password=self.PASSWORD)
        self.admin_acc = admin_acc
        self.assertTrue(login)
    
    def test_dashboard_response_with_unverified_lowongan(self):
        response = self.client.get(DASHBOARD)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_proposal.html')
        self.assertEqual(response.context['msg'], 1)
    
    def test_dashboard_response_with_no_unverified_lowongan(self):
        self.lowongan.status = Lowongan.StatusLowongan.VERIFIED
        self.lowongan.save()
        response = self.client.get(DASHBOARD)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_proposal.html')
        self.assertEqual(response.context['msg'], 'Tidak Ada Request Proposal Lowongan')

    def test_verifikasi_response_with_verified_lowongan(self):
        self.lowongan.status = Lowongan.StatusLowongan.VERIFIED
        self.lowongan.save()
        response = self.client.get(TERVERIFIKASI)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'terverifikasi.html')
        self.assertEqual(response.context['msg'], 1)
    
    def test_verifikasi_response_with_no_verified_lowongan(self):
        self.lowongan.status = Lowongan.StatusLowongan.UNVERIFIED
        self.lowongan.save()
        response = self.client.get(TERVERIFIKASI)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'terverifikasi.html')
        self.assertEqual(response.context['msg'], 'Tidak Ada Proposal Lowongan Yang Terverifikasi')

    def test_riwayat_response_with_lowongan(self):
        response = self.client.get(RIWAYAT)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'riwayat.html')
        self.assertEqual(response.context['msg'], 1)

    def test_riwayat_response_with_no_lowongan(self):
        self.lowongan.delete()
        response = self.client.get('/dashboard-proposal-lowongan/riwayat')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'riwayat.html')
        self.assertEqual(response.context['msg'], 'Tidak Ada Riwayat Proposal Lowongan')

    def test_detail_page(self):
        url = reverse(DETAIL, args=[self.lowongan.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_page.html')
        self.assertEqual(response.context['msg'], 'Tersedia')
