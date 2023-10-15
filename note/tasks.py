from celery import shared_task

from . import models, services

from datetime import datetime, timezone

from django.conf import settings

from django.template.loader import get_template

# Email
# from django.core.mail import send_mail


@shared_task
def send_mm_mail(note):
    print("IN Send Email async.....")
    pass
    # Generate template
    # html_template = get_template("reminder.html").render(context)

    # # Email data
    # email_data = {
    #     "subject": "Note reminder",
    #     "to": note.user.email,
    # }

    # # Send template to mail
    # services.send_email(html_template, email_data)

    send_mail(
        html_message="This is  body",
        fail_silently=False,
        subject="hello reminder",
        recipient_list=["michotall95@gmail.com"],
        from_email=settings.EMAIL_HOST_USER,
        # message="html_message",
    )


@shared_task
def due_date_reminder():
    print("Reminder Celery here")

    # current time
    cur_time = datetime.now(timezone.utc)

    # Get only notes that have not passed thier due date
    notes = models.Note.objects.filter(due_date__gt=cur_time, is_email_send=False)

    for note in notes:
        time_result = (note.due_date - cur_time).total_seconds() / 60
        print(f"{time_result}  {note.user.email} {note.is_email_send} {note.title}")
        if (time_result > 30 and time_result < 31) and (note.is_email_send == False):
            # Get url domain from settings
            current_site = settings.DOMAIN_LINK

            absolute_url = "http://" + current_site + f"/api/notes/note/{str(note.id)}"

            #  Get html context
            context = {
                "title": note.title,
                "link": absolute_url,
                "user_name": f"{note.user.last_name} {note.user.first_name}",
            }

            # Generate template
            html_template = get_template("notes.html").render(context)

            # Email data
            email_data = {
                "subject": "Note reminder",
                "to": note.user.email,
            }

            # # # Send template to mail
            # EmailMessage(
            #     body="This is  body",
            #     subject="hello reminder",
            #     to=["michotall95@gmail.com"],
            #     from_email=settings.EMAIL_HOST_USER,
            # )
            services.send_email(html_template, email_data)

            # Change note is_email send to true
            services.update_note_is_email_send(note.id)
            print(f"send mail.... {note.title}")
