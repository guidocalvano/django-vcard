# Create your views here.
from django.shortcuts import render_to_response

def vCardForm( request ) :
    
    renderToResponse( 'vCardForm.html', {} ) ;




def hCard( request ) :
    
    vCardString = request.POST[ 'vCard' ]
    
    contact = Contact( vCardString ) 
    
    renderToResponse( 'vCardForm.html', { 'contact' : contact } ) ;
