from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    hashed_identifier = models.CharField(max_length=255, unique=True)
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=10, default="sw")
    consent_data_use = models.BooleanField(default=False)
    consent_research = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.hashed_identifier
