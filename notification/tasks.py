from jobseeker.celery import app
from celery.schedules import crontab
from jobseeker.models import Lowongan, Users
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from jobseeker.settings import HOSTNAME


@app.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=9, minute=0), notify_job_vacancy_task)


@app.task(bind=True)
def notify_job_vacancy_task(self):
    # get all job that are open today
    open_job_vacancy = Lowongan.objects.all_open_lowongan().filter(
        buka_lowongan=timezone.now().date()
    )[:6]
    html_message = render_to_string(
        "new_vacancy.html",
        {"open_job_vacancy": open_job_vacancy, "hostname": HOSTNAME},
    )
    plain_message = strip_tags(html_message)

    if len(open_job_vacancy) == 0:
        return

    # notify all subscribed user
    subscribed_user = map(lambda x: x["email"], Users.objects.filter(subscribed=True).values("email"))

    return send_mail(
        from_email="tracerstudyteknokrat@gmail.com",
        subject="Lowongan Baru dibuka!",
        message=plain_message,
        html_message=html_message,
        recipient_list=subscribed_user,
    )
