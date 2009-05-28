from alaska.teikningar.models import Teikning, DeepZoom, Umfjollun, Frasogn, Ljosmynd, Scan
from django.contrib import admin
from django import forms
from string import Template
from django.utils.safestring import mark_safe
from django.conf import settings
import os

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
     
    
class SelectScansWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        scansDir = 'E:/backup/www/bthj.is/alaska/teikningar'
        files = os.listdir(scansDir)
        scansList = []
        for f in files:
            if os.path.isfile(os.path.join(scansDir,f)):
                print f
                scansList.append(f)
        selectTemplate = Template(u"""<select name="$name" id="$name">""")
        optionTemplate = Template(u"""<option value="$scanValue">$scanOption</option>""")
        returnValue = selectTemplate.substitute(name=name)
        for videoChoice in scansList:
            returnValue += optionTemplate.substitute(scanValue=videoChoice, scanOption=videoChoice)
        returnValue += "</select>"
        return mark_safe(returnValue)

class ScanAdminForm(forms.ModelForm):
    class Meta:
        model = Teikning
    scan = forms.CharField(widget=SelectScansWidget())
    #scan = forms.ChoiceField(choices=videoChoices)
        
class ScanInine(admin.TabularInline):
    model = Scan
    form = ScanAdminForm
    extra = 1

class TeikningAdmin(admin.ModelAdmin):
    inlines = [UmfjollunInline, FrasognInline, DeepZoomInline, ScanInine, LjosmyndInline]
    list_display = ('dags', 'eigandi', 'stadur')
    list_filter = ['sveitarfelag', 'flokkur', 'skipulag', 'teikning']
    search_fields = ['eigandi','stadur','sveitarfelag','flokkur','flokkur_nanar','skipulag','teikning']
    date_hierarchy = 'dags'

admin.site.register(Teikning, TeikningAdmin)
admin.site.register(Scan)