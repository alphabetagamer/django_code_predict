from django.db import models
from django.contrib.auth.models import User


class code_page(models.Model):
    langs = [("Python", "Python")]
    lang = models.CharField(choices=langs, default="Python", max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    content = models.CharField(max_length=255, default="http://www.google.com")

    def __str__(self):
        return self.title


class progress(models.Model):
    user = models.CharField(max_length=255)
    id_code = models.IntegerField(null=True)
    prog = models.CharField(max_length=255)

    def __str__(self):
        return self.user