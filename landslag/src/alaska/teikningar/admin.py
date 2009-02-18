from alaska.teikningar.models import Teikning, DeepZoom, Umfjollun, Frasogn, Ljosmynd, Scan
from django.contrib import admin

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
        
class ScanInine(admin.TabularInline):
    model = Scan
    extra = 1

class TeikningAdmin(admin.ModelAdmin):
    inlines = [UmfjollunInline, FrasognInline, DeepZoomInline, ScanInine, LjosmyndInline]
    list_display = ('dags', 'eigandi', 'stadur')
    list_filter = ['sveitarfelag', 'flokkur', 'skipulag', 'teikning']
    search_fields = ['eigandi','stadur','sveitarfelag','flokkur','flokkur_nanar','skipulag','teikning']
    date_hierarchy = 'dags'

admin.site.register(Teikning, TeikningAdmin)