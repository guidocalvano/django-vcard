from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
import vobject
from vobject.vcard import *
from django.shortcuts import render_to_response
import StringIO

def select(request):
    return render_to_response(
        "admin/vCard/uploadVCard.html",
        {},
        RequestContext(request, {}),
    )
select = staff_member_required(select)


def vcf_file_view(request,contact_set):

    vcf_file_content = ""

    for c in contact_set :

        vcf_file_content = vcf_file_content + c.convertTo( 'vCard' )

    theFile = StringIO.StringIO()

    theFile.write( vcf_file_content ) 

    response = HttpResponse(FileWrapper(theFile), mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=vcf_file.vcf'
    return response



def loadFile(request):
    
    
    
    return render_to_response(
        "admin/vCard/uploadVCard.html",
        {},
        RequestContext(request, {}),
    )
loadFile = staff_member_required(loadFile)