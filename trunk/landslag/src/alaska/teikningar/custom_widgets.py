from django import forms
from django.template import Context, Template
from django.conf import settings
from alaska.teikningar.models import Scan, Ljosmynd, Frasogn, Myndband
import os

class SelectWidgetAuxiliary():
    @classmethod
    def getFileListRegisteredInDB(cls, modelObject, modelColumn):
        scan_list = [eval("r."+modelColumn) for r in modelObject.objects.all()]
        return sorted(scan_list)
    
    @classmethod
    def getFileListFromFilesystem(cls, filesDir, truncateCount):
        files = os.listdir(filesDir)
        scansList = []
        for f in files:
            if os.path.isfile(os.path.join(filesDir,f)):
                scansList.append(f[:-truncateCount]) 
        return sorted(scansList)
    
    @classmethod
    def renderListsToSelect(cls, toPickList, alreadyPickedList, name, value):
        strTemp = """<select name="{{name}}" id="{{name}}">
                        <option value=""></option>
                        {% for optgroup in groups %}
                        <optgroup label="{% autoescape off %}{{optgroup.name}}{% endautoescape %}">
                            {% for option in optgroup.options %}
                            <option value="{{option.value}}"{% if option.selected %} selected="selected"{% endif %}>
                                {{ option.name }}
                            </option>
                            {% endfor %}
                        </optgroup>
                        {% endfor %}
                    </select>"""
        t = Template(strTemp)
        groups = [{"name":"&aacute eftir a&eth; skr&aacute;","options":[]},
                  {"name":"&thorn;egar skr&aacute;&eth; &iacute; grunn","options":[]}]
        for pick in toPickList:
            countAlreadyPicked = alreadyPickedList.count(pick)
            option = {"name": (countAlreadyPicked > 0 and 'x: '.join([str(countAlreadyPicked),pick]) or pick), 
                      "selected":(pick==value and True or None), 
                      "value":pick}
            groups[(countAlreadyPicked > 0 and 1 or 0)]["options"].append(option)
        return t.render(Context({"name":name,"groups":groups}))        


class SelectScansWidget(forms.TextInput, SelectWidgetAuxiliary):
    scansDir = settings.SCAN_FILES_DIR
    def render(self, name, value, attrs=None):
        scanListFromFilesystem = self.getFileListFromFilesystem( self.scansDir, 5 ) #truncate .html = 5
        # scanListFromDB = Scan.objects.values_list('scan', flat=True).order_by('scan')
        scanListFromDB = self.getFileListRegisteredInDB( Scan, "scan" )
        return self.renderListsToSelect( scanListFromFilesystem, scanListFromDB, name, value )
    
class SelectLjosmyndWidget(forms.TextInput, SelectWidgetAuxiliary):
    ljosmyndDir = settings.LJOSMYND_FILES_DIR
    def render(self, name, value, attrs=None):
        ljosmyndListFromFilesystem = self.getFileListFromFilesystem( self.ljosmyndDir, 4 )  # .jpg = 4
        ljosmyndListFromDB = self.getFileListRegisteredInDB( Ljosmynd, "ljosmynd" )
        return self.renderListsToSelect( ljosmyndListFromFilesystem, ljosmyndListFromDB, name, value )
    
class SelectFrasognWidget(forms.TextInput, SelectWidgetAuxiliary):
    frasognDir = settings.FRASOGN_FILES_DIR
    def render(self, name, value, attrs=None):
        frasognListFromFilesystem = self.getFileListFromFilesystem( self.frasognDir, 4 )
        frasognListFromDB = self.getFileListRegisteredInDB( Frasogn, "frasogn" )
        return self.renderListsToSelect( frasognListFromFilesystem, frasognListFromDB, name, value )

class SelectMyndbandWidget(forms.TextInput, SelectWidgetAuxiliary):
    myndbandDir = settings.MYNDBAND_FILES_DIR
    def render(self, name, value, attrs=None):
        myndbandListFromFilesystem = self.getFileListFromFilesystem( self.myndbandDir, 4 )
        myndbandListFromDB = self.getFileListRegisteredInDB( Myndband, "myndband" )
        return self.renderListsToSelect( myndbandListFromFilesystem, myndbandListFromDB, name, value)
