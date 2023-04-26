from django.test import TestCase
from ..models import Users
from ..queryset import LowonganQuerySet
from django.utils import timezone
from datetime import  timedelta

class LowonganQuerySetTestCase(TestCase):

    def setUp(self):
        self.perusahaan = Users.objects.create (
            username="perusahaan",
            password="password",
            npm=2,
            prodi_id=2,
            role_id=2
        )

        self.queryset = LowonganQuerySet(model=Lowongan, using='default')



    def update_status_by_date_should_change_lowongan_status_to_buka_if_valid(self):
        should_open = self.queryset.create(
                users_id=self.perusahaan,
                posisi="Software engineer",
                status="Sudah terverifikasi",
                lama_pengalaman=10,
                gaji=100,
                buka_lowongan=timezone.now().date(),
                batas_pengumpulan=timezone.now().date() + timedelta(days=1)
        )

        self.queryset._update_status_by_date()

        should_open = self.queryset.get(id=should_open.id)

        self.assertEquals(should_open.status, 'Buka')


    def update_status_by_date_should_change_lowongan_status_to_tutup_if_already_closed(self):
        
        self.should_close = self.queryset.create(
                users_id=self.perusahaan,
                posisi="Software engineer",
                status="Buka",
                lama_pengalaman=10,
                gaji=100,
                buka_lowongan=timezone.now().date() - timedelta(days=1),
                batas_pengumpulan=timezone.now().date() - timedelta(days=2)
        )

        self.queryset._update_status_by_date()

        should_close = self.queryset.get(id=should_close.id)

        self.assertEquals(should_close.status, 'Tutup')

    def all_open_lowongan_should_return_lowongan_with_open_status(self):
        all_lowongan = self.queryset.all_open_lowongan()

        for lowongan in all_lowongan:
            self.assertEquals(lowongan.status, 'Buka')

    def search_should_return_query_with_appropriate_result(self):
        searched_lowongan = self.queryset.search('software')

        for lowongan in searched_lowongan:
            self.assertEquals(lowongan.posisi , "Software engineer")