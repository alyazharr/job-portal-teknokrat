from django.test import TestCase, Client
from jobseeker.models import Users,Lowongan
from django.urls import reverse
from django.utils import timezone
from .tasks import notify_job_vacancy_task
from datetime import  timedelta

class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.alumni = Users.objects.create(
            subscribed=False,
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1,
        )

        self.perusahaan = Users.objects.create(
            username="perusahaan", password="password", npm=2, prodi_id=2, role_id=2
        )

        self.subscribed_alumni = Users.objects.create(
            subscribed=True,
            username="subscriber",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1,
        )

        self.url = "subscription"

        self.client = Client()

    def test_alumni_should_be_able_to_subscribe(self):
        self.client.login(username="alumni", password="password")

        subscribe_response = self.client.get(reverse(self.url))
        subscribed_alumni = Users.objects.get(username="alumni")
        # should be subscribed since the user has not subscribed previously
        self.assertTrue(subscribed_alumni.subscribed)

    def test_other_role_than_alumni_should_not_be_able_to_subscribe(self):
        self.client.login(username="perusahaan", password="password")
        subscribe_response = self.client.get(reverse(self.url))
        self.assertEqual(subscribe_response.status_code, 403)

    def test_if_user_already_subscribe_then_it_should_unsubscribe(self):
        self.client.login(username="subscriber", password="password")
        subscribe_response = self.client.get(reverse(self.url))
        unsubscribe_alumni = Users.objects.get(username="subscriber")
        self.assertTrue(not unsubscribe_alumni.subscribed)


class NotifyVacancyTest(TestCase):

    def setUp(self):
        self.alumni = Users.objects.create (
            username="alumni",
            password="password",
            npm=1,
            prodi_id=1,
            role_id=1,
            email="test@test.com",
            subscribed=True
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

