# coding=UTF-8

from django.db import models
import os
from django.conf import settings

class Teikning(models.Model):
    dags = models.DateField('Dagsetning')
    eigandi = models.CharField('Eigandi', max_length=50, blank=True)
    stadur = models.CharField('Staður', max_length=50, blank=True)
    sveitarfelag = models.CharField('Sveitarfélag', max_length=50, blank=True)
    flokkur = models.CharField('Flokkur', max_length=5, blank=True)
    flokkur_nanar = models.CharField('Flokkur nánar', max_length=50, blank=True)
    skipulag = models.CharField('Skipulag', max_length=50, blank=True)
    teikning = models.CharField('Teikning', max_length=50, blank=True)
    frumrit = models.BooleanField('Frumrit', blank=True)
    afrit = models.BooleanField('Afrit', blank=True)
    fj_blada = models.IntegerField('Fjöldi blaða', blank=True)
    def __unicode__(self):
        return str(self.dags) + ', ' + self.eigandi + ', ' + self.stadur 
    
    class Meta:
        verbose_name_plural = "Teikningar"
    
class Umfjollun(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun', default=1)
    umfjollun = models.TextField('Umfjöllun', blank=True)
    class Meta:
        ordering = ['rodun']
        verbose_name_plural = "Umfjallanir"

class Frasogn(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun', default=1)
    frasogn = models.CharField('Frásögn', max_length=255)
    class Meta:
        ordering = ['rodun']
        verbose_name_plural = "Frásagnir"

class Ljosmynd(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun', default=1)
    ljosmynd = models.CharField('Ljósmynd', max_length=255)
    class Meta:
        ordering = ['rodun']
        verbose_name_plural = "Ljósmyndir"

class Scan(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun',default=1)
    scan = models.CharField('Skann', max_length=255)
    class Meta:
        ordering = ['rodun']
        verbose_name_plural = "Skönn"
        
class Myndband(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun',default=1)
    myndband = models.CharField('Myndband', max_length=255)
    class Meta:
        ordering = ['rodun']
        verbose_name_plural = "Myndbönd"