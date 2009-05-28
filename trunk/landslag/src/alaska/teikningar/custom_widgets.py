from django import forms
from string import Template
from django.utils.safestring import mark_safe
from django.conf import settings
from alaska.teikningar.models import Scan
import os

class SelectScansWidget(forms.TextInput):
    def getScanListRegisteredInDB(self):
        scan_list = [r.scan for r in Scan.objects.all()]
        return scan_list
    
    def getScanListFromFilesystem(self):
        scansDir = settings.SCAN_FILES_DIR
        files = os.listdir(scansDir)
        scansList = []
        for f in files:
            if os.path.isfile(os.path.join(scansDir,f)):
                scansList.append(f)
        return scansList        
    
    def render(self, name, value, attrs=None):
        scanListFromFilesystem = self.getScanListFromFilesystem()
        scanListFromDB = self.getScanListRegisteredInDB()
        selectTemplate = Template(u"""<select name="$name" id="$name"><option value=""></option>""")
        optionTemplate = Template(u"""<option value="$scanValue"$selected>$scanOption</option>""")
        returnValue = selectTemplate.substitute(name=name)
        optionsInFilesystemOnly = ''
        optionsAlreadyInDB = ''
        for scan in scanListFromFilesystem:
            countScanInDB = scanListFromDB.count(scan)
            if scan == value:
                selected = ' selected="selected"'
            else:
                selected  = ''
            if countScanInDB > 0:
                optionsAlreadyInDB += optionTemplate.substitute(scanValue=scan, scanOption='x'+str(countScanInDB)+': '+scan, selected=selected)
            else:
                optionsInFilesystemOnly += optionTemplate.substitute(scanValue=scan, scanOption=scan, selected=selected)
        returnValue += """<optgroup label="&aacute eftir a&eth; skr&aacute;">""" + optionsInFilesystemOnly + "</optgroup>"
        returnValue += """<optgroup label="&thorn;egar skr&aacute;&eth; &iacute; grunn">""" + optionsAlreadyInDB + "</optgroup>"
        returnValue += "</select>"
        return mark_safe(returnValue)