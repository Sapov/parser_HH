from django.db import models


class Parser(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=255)
    vacancy_description = models.TextField()
    company = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    add_date = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.title

