from django.db import models
from django.conf import settings

class Reference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    note = models.TextField()
    link = models.CharField(max_length=300)
    last_modified = models.DateTimeField()

    def __str__(self):
        return self.title
