from django import template
from teikningar import models

register = template.Library()

@register.inclusion_tag('scans.html')
def display_scans(teikning_id):
    teikning = models.Teikning.objects.get(id__exact=teikning_id)
    scans = models.Scan.objects.filter(teikning=teikning)
    return { 'scans' : scans }