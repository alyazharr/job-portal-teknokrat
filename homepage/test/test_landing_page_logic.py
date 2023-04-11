from django.test import TestCase, Client
from django.urls import reverse
from jobseeker.models import Users

LANDING_PAGE = '/'

class LandingPageTestNoLogin(TestCase):
    def test_landing_page_redirect(self):
        response = self.client.get(LANDING_PAGE)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertFalse(response.context['user'].is_authenticated)

class LandingPageTestAlumni(TestCase):
    PASSWORD_ALUMNI = "alumnibeneran123"
    NAME_ALUMNI = "Dummy alumni"
    USERNAME_ALUMNI = "alumni-beneran"
    NPM_ALUMNI = 12345678
    PRODI_ID_ALUMNI = 84202
    
    def setUp(self) -> None:
        super().setUp()

        self.client = Client()
        alumni_acc = Users.objects.create(
            username=self.USERNAME_ALUMNI,
            password=self.PASSWORD_ALUMNI,
            name=self.NAME_ALUMNI,
            npm=self.NPM_ALUMNI,
            prodi_id=self.PRODI_ID_ALUMNI,
            role_id=1
        )

        self.alumni_acc = alumni_acc
        login = self.client.login(username=self.USERNAME_ALUMNI,password=self.PASSWORD_ALUMNI)       
        self.assertTrue(login)

    def test_landing_page_redirect(self):
        response = self.client.get(LANDING_PAGE)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].role_id, 1)

class LandingPageTestPerusahaan(TestCase):
    PASSWORD_PERUSAHAAN = "Perusahaanbeneran123"
    NAME_PERUSAHAAN = "Dummy perusahaan"
    USERNAME_PERUSAHAAN = "perusahaan-beneran"
    NPM_PERUSAHAAN = 12345678
    PRODI_ID_PERUSAHAAN = 84202
    
    def setUp(self) -> None:
        super().setUp()

        self.client = Client()
        perusahaan_acc = Users.objects.create(
            username=self.USERNAME_PERUSAHAAN,
            password=self.PASSWORD_PERUSAHAAN,
            name=self.NAME_PERUSAHAAN,
            npm=self.NPM_PERUSAHAAN,
            prodi_id=self.PRODI_ID_PERUSAHAAN,
            role_id=2
        )

        self.perusahaan_acc = perusahaan_acc
        login = self.client.login(username=self.USERNAME_PERUSAHAAN,password=self.PASSWORD_PERUSAHAAN)       
        self.assertTrue(login)

    def test_landing_page_redirect(self):
        response = self.client.get(LANDING_PAGE)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/dashboard-lowongan-pekerjaan")

class LandingPageTestAdmin(TestCase):
    PASSWORD_ADMIN = "adminadminan123"
    USERNAME_ADMIN = "admin-teknokrat1234"
    NAME_ADMIN = "Admin Dummy Beneran"
    NPM_ADMIN = 20076734
    PRODI_ID_ADMIN = 84202

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

    def test_landing_page_redirect(self):
        response = self.client.get(LANDING_PAGE)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard_proposal_lowongan:dashboard")) 
        self.assertEqual(response.url, "/dashboard-proposal-lowongan/")