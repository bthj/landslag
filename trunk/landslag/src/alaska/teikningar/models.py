# coding=UTF-8

from django.db import models

class Teikning(models.Model):
    dags = models.DateField('Dagsetning')
    eigandi = models.CharField('Eigandi', max_length=50)
    stadur = models.CharField('Staður', max_length=50)
    sveitarfelag = models.CharField('Sveitarfélag', max_length=50)
    flokkur = models.CharField('Flokkur', max_length=5)
    flokkur_nanar = models.CharField('Flokkur nánar', max_length=50)
    skipulag = models.CharField('Skipulag', max_length=50)
    teikning = models.CharField('Teikning', max_length=50)
    frumrit = models.BooleanField('Frumrit')
    afrit = models.BooleanField('Afrit')
    fj_blada = models.IntegerField('Fjöldi blaða')
    def __unicode__(self):
        return str(self.dags) + ', ' + self.eigandi + ', ' + self.stadur 
    
class Umfjollun(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun', default=1)
    umfjollun = models.TextField('Umfjöllun')

class Frasogn(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun', default=1)
    frasogn = models.FilePathField('Frásögn', path='/home/teikningar/frasagnir', recursive=True)

class Ljosmynd(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun', default=1)
    ljosmynd = models.FilePathField('Ljósmynd', path='/home/teikningar/ljosmyndir', recursive=True)
    
SCAN_TEGUND_CHOICES = (
    ('thumb', 'Smámynd'),
    ('medium', 'Meðalstærð'),
    ('large', 'Stór'),
    ('original', 'Upprunaleg stærð')
) 
class Scan(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun',default=1)
    tegund = models.CharField('Tegund', max_length=10, choices=SCAN_TEGUND_CHOICES)
    scan = models.FilePathField('Skann', path='/home/teikningar/scan', recursive=True)
    
class DeepZoom(models.Model):
    teikning = models.ForeignKey(Teikning)
    rodun = models.IntegerField('Röðun', default=1)
    deep_zoom_image = models.FilePathField('Deep Zoom mynd', path='/home/teikningar/dzi', match=".*\.dzi$", recursive=True, blank=True)