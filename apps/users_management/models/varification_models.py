import datetime

from django.db import models
from django.utils import timezone

from apps.users_management.models import UserManage
from backend.utils.text_choices import VerificationForStatus


class EmailVerification(models.Model):
    user = models.OneToOneField(UserManage, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, null=True, blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    using_for = models.CharField(
        max_length=100,
        choices=VerificationForStatus.choices,
        default=VerificationForStatus.NO_REQUEST,
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created
            self.expires_at = timezone.now() + datetime.timedelta(days=1)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Email Verification"

    def __str__(self):
        return (
            " ID "
            + str(self.id)
            + " - "
            + str(self.user.username)
            + " - "
            + str(self.user.email)
            + " - "
            + self.otp
            + " - "
            + str(self.used)
            + " - "
            + str(self.expires_at)
            + " - "
            + str(self.using_for)
        )
