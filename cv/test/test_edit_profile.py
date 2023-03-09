from django.test import TestCase, Client
from jobseeker.models import CV, Users
from django.urls import reverse
from ..views import edit_profile

class EditProfileTestCase(TestCase):
    def setUp(self):
        global CV_PROFILE_EDIT
        CV_PROFILE_EDIT = "cv:edit_profile"

        created_user = Users.objects.create(
            username="veloraine",
            password="initesting123",
            npm=1,
            prodi_id=1,
            role_id=1
        )
        CV.objects.create(
            user=created_user,
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

    def test_edit_profile_should_render_edit_profile_template(self):
        client = Client()
        client.login('veloraine', 'initesting123')
        url = reverse(CV_PROFILE_EDIT)
        response = client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cv/edit_profile.html')


    def test_edit_profile_should_change_field(self):
        client = Client()
        client.login('veloraine', 'initesting123')
        url = reverse(CV_PROFILE_EDIT)
        response = client.post(url, {'profile': 'profile2'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['cv'].profile, 'profile2')

    def test_edit_profile_should_redirect_to_profile(self):
        client = Client()
        client.login('veloraine', 'initesting123')
        url = reverse(CV_PROFILE_EDIT)
        response = client.post(url, {'profile': 'profile3'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/cv/profile/')
        self.assertEquals(response.context['cv'].profile, 'profile3')
    
    def test_edit_profile_should_return_404_if_user_is_not_logged_in(self):
        client = Client()
        url = reverse(CV_PROFILE_EDIT)
        response = client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_edit_profile_should_use_view_edit_profile(self):
        client = Client()
        client.login('veloraine', 'initesting123')
        url = reverse(CV_PROFILE_EDIT)
        response = client.get(url)
        self.assertEquals(response.resolver_match.func, edit_profile)



