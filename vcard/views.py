# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from vCard.models import Contact


def vCardForm(request):
    render_to_response('vCardForm.html', {})


def testVCardForm(request):
    if 'input' not in request.POST:
        return render_to_response('vCardFormTest.html', {'input' : '', 'output' : ''}, context_instance=RequestContext(request))

    input = request.POST['input']
    contact = Contact()
    contact.fromVCard(input)
    output = contact.toVCard()
    return render_to_response('vCardFormTest.html', {'input' : input, 'output' : output}, context_instance=RequestContext(request))


def hCard(request):
    vCardString = request.POST['vCard']
    contact = Contact(vCardString)

    render_to_response('vCardForm.html', {'contact' : contact}, context_instance=RequestContext(request))
