from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class Inscription(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    text = models.TextField('Aprašymas', max_length=1000, help_text='Užrašo aprašymas')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Užrašas'
        verbose_name_plural = 'Užrašai'

class Category(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text='Įveskite užrašo kategoriją')
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategorija'
        verbose_name_plural = 'Kategorijos'

    def display_inscriptions(self):
        return ', '.join(inscription.title for inscription in self.inscription_set.all()[:3])

    display_inscriptions.short_description = 'Knygos'