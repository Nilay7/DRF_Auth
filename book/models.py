from django.db import models

# Create your models here.
class Books(models.Model):
    #title of book
    title = models.CharField(max_length = 255, null = False)
    #author of book
    author = models.CharField(max_length = 255, null = False)

    def __str__(self):
        return '{} - {}'.format(self.title, self.author)