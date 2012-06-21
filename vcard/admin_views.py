from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
import vobject
from vobject.vcard import *
from django.shortcuts import render_to_response
import StringIO
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper


def vcf_file_view(request, contact_set):
    vcf_file_content = ""

    for c in contact_set :

        vcf_file_content = vcf_file_content + c.exportTo('vCard')

    theFile = StringIO.StringIO()

    theFile.write(vcf_file_content)
    theFile.seek(0)

    response = HttpResponse(vcf_file_content, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=vcf_file.vcf'

    return response

vcf_file_view = staff_member_required(vcf_file_view)
