from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="user", on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=220, null=False, blank=False, verbose_name="Title"
    )

    content = models.TextField(null=False, blank=False, verbose_name="content")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date created")

    due_date = models.DateTimeField(verbose_name="due date", blank=False, null=False)

    is_complete = models.BooleanField(default=False, verbose_name="is complete")

    is_email_send = models.BooleanField(default=False, verbose_name="is email send")

    priority = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Priority",
    )

    def __str__(self) -> str:
        return self.title
