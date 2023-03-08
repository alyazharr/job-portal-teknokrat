from django.test import TestCase, Client
from jobseeker.models import CV, Users

class UsersManagerTestCase(TestCase):

    def test_profile_if_user_is_logged_in(self):
        created_user = Users.objects.create(
            username="username",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1
        )
        created_cv = CV.objects.create(
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

        client = Client()
        client.login(username="username",password="password")
        response = client.get("/profile/")
        assert response.status_code == 200

    def test_profile_if_user_is_not_logged_in(self):
        pass

    def test_profile_should_return_certain_attribute(self):
        pass

    def test_profile_should_render_profile_template(self):
        pass

    def test_edit_profile_should_render_edit_profile_template(self):
        pass

    def test_edit_profile_should_change_field(self):
        pass

