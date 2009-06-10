#!python
# coding=utf-8
from alaska.teikningar.models import Teikning, Umfjollun, Frasogn, Ljosmynd, Scan, Myndband
from django.contrib import admin
from django import forms
from custom_widgets import SelectScansWidget, SelectFrasognWidget, SelectLjosmyndWidget, SelectMyndbandWidget
    
class UmfjollunInline(admin.StackedInline):
    model = Umfjollun
    extra = 1
    
class FrasognAdminForm(forms.ModelForm):
    class Meta:
        model = Frasogn
    frasogn = forms.CharField(widget=SelectFrasognWidget())
class FrasognInline(admin.TabularInline):
    model = Frasogn
    form = FrasognAdminForm
    extra = 1
    
class LjosmyndAdminForm(forms.ModelForm):
    class Meta:
        model = Ljosmynd
    ljosmynd  = forms.CharField(widget=SelectLjosmyndWidget())
class LjosmyndInline(admin.TabularInline):
    model = Ljosmynd
    form = LjosmyndAdminForm
    extra = 1

class ScanAdminForm(forms.ModelForm):
    class Meta:
        model = Scan
    scan = forms.CharField(widget=SelectScansWidget())    
class ScanInine(admin.TabularInline):
    model = Scan
    form = ScanAdminForm
    extra = 1
    
class MyndbandAdminForm(forms.ModelForm):
    class Meta:
        model = Myndband
    myndband = forms.CharField(widget=SelectMyndbandWidget())
class MyndbandInline(admin.TabularInline):
    model = Myndband
    form = MyndbandAdminForm
    extra = 1


class TeikningAdmin(admin.ModelAdmin):
    inlines = [ScanInine, UmfjollunInline, FrasognInline, LjosmyndInline, MyndbandInline]
    list_display = ('hasTeikningar', 'dags', 'eigandi', 'stadur')
    list_filter = ['flokkur', 'sveitarfelag', 'skipulag', 'teikning']
    search_fields = ['eigandi','stadur','sveitarfelag','flokkur','flokkur_nanar','skipulag','teikning']
    date_hierarchy = 'dags'
    list_display_links = ['dags']
    
    def hasTeikningar(self, obj):
        return len(Scan.objects.filter(teikning=obj)) > 0
    hasTeikningar.boolean = True
    hasTeikningar.short_description = 'Skannað'

admin.site.register(Teikning, TeikningAdmin)
admin.site.register(Scan)