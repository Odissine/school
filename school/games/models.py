import os

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.files.storage import FileSystemStorage
from .storage import OverwriteStorage

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


class Word(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    level = models.IntegerField(default=1)
    image = models.ImageField(upload_to='', storage=fs)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Mot'
        verbose_name_plural = 'Mots'

    # Methode d'enregistrement dans la base ... On ajoute le champ slug
    def save(self, *args, **kwargs):
        # On check si Object Mot déjà créé
        # On test ensuite si l'image de la base est identique à celle envoyée par le formulaire
        # Si différent on supprime l'ancien fichier pour uploader le nouveau lors de la sauvegarde du modèle
        try:
            this = Word.objects.get(pk=self.id)
            if this.image != self.image:
                this.image.delete()
        except:
            this = self

        extension = self.image.name.split(".")[-1].lower()
        self.slug = slugify(self.name)
        self.image.name = "word/" + self.slug + "." + extension

        # Si le fichier existe on le renomme avec la valeur du nouveau mot (cas ou seul le mot change ... pas le fichier)
        if os.path.exists(settings.MEDIA_ROOT + "/" + this.image.name):
            os.rename(settings.MEDIA_ROOT + "/" + this.image.name, settings.MEDIA_ROOT + '/word/' + slugify(self.name) + "." + extension)

        super(Word, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('games:word', args=[self.slug])

    def delete_file(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        print(storage, path)
        storage.delete(path)


class WordFind(models.Model):
    objects = models.Manager()
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.word.name


class LetterScore(models.Model):
    objects = models.Manager()
    score = models.IntegerField()
    level = models.CharField(max_length=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __int__(self):
        return self.score


class AdditionScore(models.Model):
    objects = models.Manager()
    score = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __int__(self):
        return self.score


class AdditionPoseeScore(models.Model):
    objects = models.Manager()
    score = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __int__(self):
        return self.score


class MultiplicationScore(models.Model):
    objects = models.Manager()
    score = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __int__(self):
        return self.score


class SoustractionScore(models.Model):
    objects = models.Manager()
    score = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __int__(self):
        return self.score


class Halo(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='', storage=fs)

    # Methode d'enregistrement dans la base ...
    def save(self, *args, **kwargs):
        # On check si Object Mot déjà créé
        # On test ensuite si l'image de la base est identique à celle envoyée par le formulaire
        # Si différent on supprime l'ancien fichier pour uploader le nouveau lors de la sauvegarde du modèle
        try:
            this = Halo.objects.get(pk=self.pk)
            if this.image != self.image:
                this.image.delete()
        except:
            this = self

        extension = self.image.name.split(".")[-1].lower()
        self.image.name = "halo/" + slugify(self.name) + "." + extension

        # Si le fichier existe on le renomme avec la valeur du nouveau mot (cas ou seul le mot change ... pas le fichier)
        if os.path.exists(settings.MEDIA_ROOT + "/" + this.image.name):
            os.rename(settings.MEDIA_ROOT + "/" + this.image.name, settings.MEDIA_ROOT + '/halo/' + slugify(self.name) + "." + extension)

        super(Halo, self).save(*args, **kwargs)
