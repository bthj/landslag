from django.db import models

class Teikning(models.Model):
    dags = models.DateField()
    eigandi = models.CharField(max_length=50)
    stadur = models.CharField(max_length=50)
    sveitarfelag = models.CharField(max_length=50)
    flokkur = models.CharField(max_length=5)
    flokkur_nanar = models.CharField(max_length=50)
    skipulag = models.CharField(max_length=50)
    teikning = models.CharField(max_length=50)
    frumrit = models.BooleanField()
    afrit = models.BooleanField()
    fj_blada = models.IntegerField()
    
class Umfjollun(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField(default=1)
    umfjollun = models.TextField()

class Frasogn(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField(default=1)
    frasogn = models.FilePathField(path='/home/teikningar/frasagnir', recursive=True)

class Ljosmynd(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField(default=1)
    ljosmynd = models.FilePathField(path='/home/teikningar/ljosmyndir', recursive=True)
    
SCAN_TEGUND_CHOICES = (
    ('thumb', 'Smámynd'),
    ('medium', 'Meðalstærð'),
    ('large', 'Stór'),
    ('original', 'Upprunaleg stærð')
) 
class Scan(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField(default=1)
    tegund = models.CharField(max_length=10, choices=SCAN_TEGUND_CHOICES)
    ljosmynd = models.FilePathField(path='/home/teikningar/scan', recursive=True)
