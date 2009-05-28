from alaska.teikningar.models import Teikning, DeepZoom, Umfjollun, Frasogn, Ljosmynd, Scan
from django.contrib import admin
from django import forms
from custom_widgets import SelectScansWidget

class DeepZoomInline(admin.TabularInline):
    model = DeepZoom
    extra = 1
    
class UmfjollunInline(admin.StackedInline):
    model = Umfjollun
    extra = 1
    
class FrasognInline(admin.TabularInline):
    model = Frasogn
    extra = 1
    
class LjosmyndInline(admin.TabularInline):
    model = Ljosmynd
    extra = 1


class ScanAdminForm(forms.ModelForm):
    class Meta:
        model = Teikning
    scan = forms.CharField(widget=SelectScansWidget())
        
class ScanInine(admin.TabularInline):
    model = Scan
    form = ScanAdminForm
    extra = 1


class TeikningAdmin(admin.ModelAdmin):
    inlines = [ScanInine, UmfjollunInline, FrasognInline, DeepZoomInline, LjosmyndInline]
    list_display = ('dags', 'eigandi', 'stadur')
    list_filter = ['sveitarfelag', 'flokkur', 'skipulag', 'teikning']
    search_fields = ['eigandi','stadur','sveitarfelag','flokkur','flokkur_nanar','skipulag','teikning']
    date_hierarchy = 'dags'

admin.site.register(Teikning, TeikningAdmin)
admin.site.register(Scan)