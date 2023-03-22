from django.test import TestCase, Client
from jobseeker.models import Users, Lowongan
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import datetime, timedelta
import json

global VERIFIKASI_PROSES
VERIFIKASI_PROSES = 'dashboard_proposal_lowongan:verifikasi_proses'

global VERIFIKASI
VERIFIKASI = 'verifikasi'

global TOLAK
TOLAK = 'tolak'

global UNRECOGNIZE
UNRECOGNIZE = 'ngapain'

global POSISI
POSISI = "Data Scientist"

global DESKRIPSI
DESKRIPSI = "Ahli dalam bidang data dan ML"

global DATE_FORMAT
DATE_FORMAT = "%Y-%m-%d"

class BaseTestCase(TestCase):
    PASS_INSTANSI = "Perusahaan12312312345678"
    USNAME_INSTANSI = "iniperusahaansaya"
    NPM_INSTANSI = 34567230
    PRODI_INSTANSI = 8992
    ROLE_ID_INSTANSI = 2

    def setUp(self) -> None:
        self.perusahaan = Users.objects.create(
            username=self.USNAME_INSTANSI,
            password=self.PASS_INSTANSI,
            npm=self.NPM_INSTANSI,
            prodi_id=self.PRODI_INSTANSI,
            role_id=self.ROLE_ID_INSTANSI
        )

        self.lowongan = Lowongan.objects.create(
            users_id=self.perusahaan,
            posisi="Software Engineer",
            gaji=1200000,
            lama_pengalaman=8,
            deskripsi="Ahli mengoding banget",
            requirements="bisa ngoding deh",
            buka_lowongan=datetime.today().strftime(DATE_FORMAT),
            batas_pengumpulan=(datetime.today() + timedelta(days=1)).strftime(DATE_FORMAT)
        )

        self.perusahaan.save()
        self.lowongan.save()

class VerifikasiTestNoLogin(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_verifikasi_proses_response(self):
        url = reverse(VERIFIKASI_PROSES, args=[self.lowongan.id, VERIFIKASI])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_tolak_proses_response(self):
        url = reverse(VERIFIKASI_PROSES, args=[self.lowongan.id, TOLAK])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

class VerifikasiTestNotAdmin(BaseTestCase):
    PASSWORD_ALUMNI = "NotAdminAliasAlumni123"
    NAME_BUKAN_ADMIN = "Ini Bukan Admin Tapi Alumni"
    USERNAME_BUKAN_ADMIN = "sayaalumnikakbukanadmin"
    NPM_BUKAN_ADMIN = 16656878
    PRODI_ID_ALUMNI = 34567

    def setUp(self) -> None:
        super().setUp()

        self.client = Client()
        alumni_acc = Users.objects.create(
            username=self.USERNAME_BUKAN_ADMIN,
            password=self.PASSWORD_ALUMNI,
            name=self.NAME_BUKAN_ADMIN,
            npm=self.NPM_BUKAN_ADMIN,
            prodi_id=self.PRODI_ID_ALUMNI,
            role_id=1
        )
        
        self.alumni_acc = alumni_acc
        login = self.client.login(username=self.USERNAME_BUKAN_ADMIN,password=self.PASSWORD_ALUMNI)       
        self.assertTrue(login)

    def test_verifikasi_proses_response(self):
        url = reverse(VERIFIKASI_PROSES, args=[self.lowongan.id, VERIFIKASI])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage:login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Anda tidak memiliki akses ke laman ini. Silakan login sebagai Admin.')

    def test_tolak_proses_response(self):
        url = reverse(VERIFIKASI_PROSES, args=[self.lowongan.id, TOLAK])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage:login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Anda tidak memiliki akses ke laman ini. Silakan login sebagai Admin.')

class VerifikasiTestAdmin(BaseTestCase):  
    PASSWORD_ADMIN = "iniadmindeh"
    USERNAME_ADMIN = "admin-teknokrat-nih"
    NAME_ADMIN = "Admin Dummy Akun"
    NPM_ADMIN = 20012324
    PRODI_ID_ADMIN = 8420212

    def setUp(self) -> None:
        super().setUp()

        self.client = Client()
        admin_acc = Users.objects.create(
            username=self.USERNAME_ADMIN,
            password=self.PASSWORD_ADMIN,
            name=self.NAME_ADMIN,
            npm=self.NPM_ADMIN,
            prodi_id=self.PRODI_ID_ADMIN,
            role_id=4
        )

        login = self.client.login(username=self.USERNAME_ADMIN,password=self.PASSWORD_ADMIN)
        self.admin_acc = admin_acc
        self.assertTrue(login)
    
    def test_verifikasi_proses_responses_available(self):
        self.lowongan.refresh_from_db()
        self.lowongan.status = Lowongan.StatusLowongan.UNVERIFIED
        self.lowongan.status = Lowongan.StatusLowongan.VERIFIED
        url = reverse(VERIFIKASI_PROSES, args=[self.lowongan.id, VERIFIKASI])
        response = self.client.get(url)
        if response.url=="/dashboard-proposal-lowongan/":
            self.lowongan.save()
        self.lowongan.save()
        self.assertEqual(self.lowongan.status, Lowongan.StatusLowongan.VERIFIED)
        
    def test_tolak_proses_response_available(self):
        self.lowongan.refresh_from_db()
        self.lowongan.status = Lowongan.StatusLowongan.UNVERIFIED
        self.lowongan.status = Lowongan.StatusLowongan.REJECTED
        url = reverse(VERIFIKASI_PROSES, args=[self.lowongan.id, TOLAK])
        response = self.client.get(url)
        if response.url=="/dashboard-proposal-lowongan/":
            self.lowongan.save()
        self.lowongan.save()
        self.assertEqual(self.lowongan.status, Lowongan.StatusLowongan.REJECTED)

    def test_non_recognize_action(self):
        self.lowongan.status = Lowongan.StatusLowongan.UNVERIFIED
        url = reverse(VERIFIKASI_PROSES, args=[self.lowongan.id, UNRECOGNIZE])
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Perintah Tidak Dikenali')

    def test_lowongan_already_verified(self):
        self.lowongan.status = Lowongan.StatusLowongan.VERIFIED
        self.lowongan.save()
        url = reverse(VERIFIKASI_PROSES, args=[self.lowongan.id, VERIFIKASI])
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Lowongan Pekerjaan '+self.lowongan.posisi+' dari '+self.perusahaan.name+' Sudah Terverifikasi')