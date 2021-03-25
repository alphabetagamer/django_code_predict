from django.db import models
from django.contrib.auth.models import User
class code_page(models.Model):
    langs=[
    ('Python','Python'),
    ('C++','C/C++')
    ]
    lang = models.CharField(
        choices=langs,
        default='Python',
        max_length=255
    )
    title = models.CharField(
        max_length=255
    )
    desc = models.TextField()
    def __str__(self):
        return self.title