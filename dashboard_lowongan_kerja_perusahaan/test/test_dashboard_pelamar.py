from django.test import Client, TestCase
from django.urls import reverse
from jobseeker.models import Lowongan, Lamar,Users
from datetime import datetime, timedelta
import json

global LOGIN
LOGIN = 'homepage:login'

global DATE_FORMAT
DATE_FORMAT = "%Y-%m-%d"

class PelamarLowonganTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.alumni1 = Users.objects.create (
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )

        self.alumni2 = Users.objects.create (
            username="alumni2",
            password="password",
            npm=2,
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
        
        self.lamaran1 = Lamar.objects.create(
            lowongan_id = self.lowongan,
            users_id = self.alumni1,
            status ='Pending',
            created_at = datetime.today().strftime(DATE_FORMAT),
        )

        self.lamaran2 = Lamar.objects.create(
            lowongan_id = self.lowongan,
            users_id = self.alumni2,
            status ='Pending',
            created_at = datetime.today().strftime(DATE_FORMAT),
        )
    
    def test_pelamar_lowongan_logged_in(self):
        self.client.login(username='perusahaan', password='password')
        response = self.client.get(reverse('pelamar_lowongan', args=[self.lowongan.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_pelamar.html')

    def test_pelamar_lowongan_with_unauthenticated_user(self):
        self.client.login(username='alumni', password='password')
        response = self.client.get(reverse('pelamar_lowongan', args=[self.lowongan.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN)) 

    def test_terima_pelamar_with_authenticated_user(self):
        self.client.login(username='perusahaan', password='password')
        response = self.client.get(reverse('terima_pelamar', args=[self.lamaran1.id]))
        self.assertEqual(response.status_code, 302)
        self.lamaran1.refresh_from_db()
        self.assertEqual(self.lamaran1.status, 'Diterima')

    def test_tolak_pelamar_with_authenticated_user(self):
        self.client.login(username='perusahaan', password='password')
        response = self.client.get(reverse('tolak_pelamar', args=[self.lamaran2.id]))
        self.assertEqual(response.status_code, 302)
        self.lamaran2.refresh_from_db()
        self.assertEqual(self.lamaran2.status, 'Ditolak')

    def test_terima_pelamar_with_unauthenticated_user(self):
        self.client.login(username='alumni', password='password')
        response = self.client.get(reverse('terima_pelamar', args=[self.lamaran1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN)) 

    def test_tolak_pelamar_with_unauthenticated_user(self):
        self.client.login(username='alumni', password='password')
        response = self.client.get(reverse('tolak_pelamar', args=[self.lamaran2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LOGIN)) 
