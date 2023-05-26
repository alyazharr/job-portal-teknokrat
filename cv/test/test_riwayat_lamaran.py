from django.test import TestCase, Client
from django.urls import reverse
from jobseeker.models import Users, Lowongan, Lamar
from datetime import datetime, timedelta
from django.http import HttpResponse

global DATE_FORMAT
DATE_FORMAT = "%Y-%m-%d"

RIWAYAT_URL = "cv:riwayat-lamaran"

class RiwayatLamaranTestCase(TestCase):
    PASSWORD_ALUMNI = "Alumni123"
    NAME_ALUMNI = "Alumni"
    USERNAME_ALUMNI = "sayaalumni"
    NPM_ALUMNI = 1626878
    PRODI_ID_ALUMNI = 34547

    PASS_INSTANSI = "Perusahaan145678"
    USNAME_INSTANSI = "iniperusahaandia"
    NPM_INSTANSI = 345130
    PRODI_INSTANSI = 892
    ROLE_ID_INSTANSI = 2


    def setUp(self) -> None:
        super().setUp()
        
        alumni_acc = Users.objects.create(
            username=self.USERNAME_ALUMNI,
            password=self.PASSWORD_ALUMNI,
            name=self.NAME_ALUMNI,
            npm=self.NPM_ALUMNI,
            prodi_id=self.PRODI_ID_ALUMNI,
            role_id=1
        )
        
        self.alumni_acc = alumni_acc
        self.alumni_acc.save()

        self.perusahaan = Users.objects.create(
            username=self.USNAME_INSTANSI,
            password=self.PASS_INSTANSI,
            npm=self.NPM_INSTANSI,
            prodi_id=self.PRODI_INSTANSI,
            role_id=self.ROLE_ID_INSTANSI
        )

        self.lowongan = Lowongan.objects.create(
            users_id=self.perusahaan,
            posisi="Secretary",
            gaji=120000,
            lama_pengalaman=8,
            deskripsi="Ahli menulis",
            requirements="bisa ngatur jadwal saya",
            buka_lowongan=datetime.today().strftime(DATE_FORMAT),
            batas_pengumpulan=(datetime.today() + timedelta(days=1)).strftime(DATE_FORMAT)
        )

        self.lamaran = Lamar.objects.create(
            users_id=self.alumni_acc,
            lowongan_id=self.lowongan,
            status=Lamar.StatusLamaran.PENDING,
            subject="Izinkan Saya Kerja Disini",
            berkas="Ini CV Saya",    
        )

        self.perusahaan.save()
        self.lowongan.save()
        self.lamaran.save()

    def test_riwayat_no_auth(self):
        client = Client()
        url = reverse(RIWAYAT_URL)
        response = client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_riwayat_auth_as_alumni(self):
        client = Client()
        login = client.login(username=self.USERNAME_ALUMNI,password=self.PASSWORD_ALUMNI)
        self.assertTrue(login)
        url = reverse(RIWAYAT_URL)
        response = client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_riwayat_as_alumni_should_return_riwayat_template(self):
        client = Client()
        login = client.login(username=self.USERNAME_ALUMNI,password=self.PASSWORD_ALUMNI)
        self.assertTrue(login)
        url = reverse(RIWAYAT_URL)
        response = client.get(url)
        self.assertTemplateUsed(response, "riwayat_lamaran.html")
    
    def test_riwayat_as_alumni_should_return_http_response(self):
        client = Client()
        login = client.login(username=self.USERNAME_ALUMNI,password=self.PASSWORD_ALUMNI)
        self.assertTrue(login)
        url = reverse(RIWAYAT_URL)
        response = client.get(url)
        self.assertIsInstance(response, HttpResponse)

    def test_riwayat_auth_as_perusahaan(self):
        client = Client()
        login = client.login(username=self.USNAME_INSTANSI,password=self.PASS_INSTANSI)
        self.assertTrue(login)
        url = reverse(RIWAYAT_URL)
        response = client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_riwayat_auth_as_admin(self):
        PASS_ADMIN = "dummy-admin-12"
        USER_ADMIN = "admin-teknokrat-12"
        NAME_ADMIN = "Admin Dummy 123"
        NPM_ADMIN = 200767234
        PRODI_ID_ADMIN = 8421102

        admin_acc = Users.objects.create(
                username=USER_ADMIN,
                password=PASS_ADMIN,
                name=NAME_ADMIN,
                npm=NPM_ADMIN,
                prodi_id=PRODI_ID_ADMIN,
                role_id=3
        )
        admin_acc.save()
        client = Client()
        login = client.login(username=USER_ADMIN,password=PASS_ADMIN)
        self.assertTrue(login)
        url = reverse(RIWAYAT_URL)
        response = client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_riwayat_should_return_riwayat_no_lamaran(self):
        self.lamaran.delete()
        client = Client()
        login = client.login(username=self.USERNAME_ALUMNI,password=self.PASSWORD_ALUMNI)
        self.assertTrue(login)
        url = reverse(RIWAYAT_URL)
        response = client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'riwayat_lamaran.html')
        self.assertEqual(response.context['msg'], 'Tidak ada lamaran pekerjaan.')

    def test_riwayat_should_return_riwayat_available_lamaran(self):
        client = Client()
        login = client.login(username=self.USERNAME_ALUMNI,password=self.PASSWORD_ALUMNI)
        self.assertTrue(login)
        url = reverse(RIWAYAT_URL)
        response = client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'riwayat_lamaran.html')
        self.assertEqual(response.context['msg'], 1)