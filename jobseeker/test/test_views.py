from django.test import TestCase
from django.test import Client
from ..models import Users, Lowongan
from datetime import datetime, timedelta
from django.urls import reverse
import json

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
        created_lowongan = Lowongan.objects.get(pk=1)
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