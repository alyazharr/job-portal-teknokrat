from django.test import TestCase
from jobseeker.models import Users,Lowongan
from django.utils import timezone
from .tasks import notify_job_vacancy_task
from datetime import  timedelta

# Create your tests here.
class NotifyVacancyTest(TestCase):

    def setUp(self):
        self.alumni = Users.objects.create (
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1,
            email="test@test.com"
        )

           # set up perusahaan data
        self.perusahaan = Users.objects.create (
            username="perusahaan",
            password="password",
            npm=2,
            prodi_id=2,
            role_id=2
        )

        


    # positive tests
    def test_send_notification_if_any_job_opens_today(self):
        # set up lowongan data
        open_lowongan =  Lowongan.objects.create(
            users_id=self.perusahaan,
            posisi="Junior Software engineer",
            status="Buka",
            lama_pengalaman=1,
            gaji=1000,
            buka_lowongan=timezone.now().date(),
            batas_pengumpulan=timezone.now().date() + timedelta(days=1)
        )
        total_email_sent = notify_job_vacancy_task.apply().get()
        self.assertEqual(1,total_email_sent)

    
    # negative test
    def test_dont_send_notification_if_no_job_opens_today(self):
        close_lowongan = Lowongan.objects.create(
            users_id=self.perusahaan,
            posisi="Junior Software engineer",
            status="Belum terverifikasi",
            lama_pengalaman=1,
            gaji=1000,
            buka_lowongan=timezone.now().date(),
            batas_pengumpulan=timezone.now().date() + timedelta(days=1)
        )
        
        total_email_sent = notify_job_vacancy_task.apply().get()
        self.assertEqual(None,total_email_sent)

