from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
import vobject
from vobject.vcard import *

def select(request):
    return render_to_response(
        "admin/vCard/uploadVCard.html",
        {},
        RequestContext(request, {}),
    )
select = staff_member_required(select)




def loadFile(request):
    
    
    
    return render_to_response(
        "admin/vCard/uploadVCard.html",
        {},
        RequestContext(request, {}),
    )
loadFile = staff_member_required(loadFile)