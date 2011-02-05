from vcard.models import *
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from vcard.admin_views import *
import vcard
from django.shortcuts import render_to_response
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

"""
class NInline(admin.StackedInline):
    model = vcard.models.N
    max_num = 1
"""

class TelInline(admin.StackedInline):
    model = Tel
    extra = 1


class EmailInline(admin.StackedInline):
    model = Email
    extra = 1


class AdrInline(admin.StackedInline):
    model = Adr
    extra = 1


class GeoInline(admin.StackedInline):
    model = Geo
    extra = 1


class OrgInline(admin.StackedInline):
    model = Org
    extra = 1


class AgentInline(admin.StackedInline):
    model = Agent
    extra = 1


class CategoriesInline(admin.StackedInline):
    model = Categories
    extra = 1


class KeyInline(admin.StackedInline):
    model = Key
    extra = 1


class LabelInline(admin.StackedInline):
    model = vcard.models.Label
    extra = 1


# class LogoInline(admin.StackedInline):
#    model = Logo
#    extra = 1


class MailerInline(admin.StackedInline):
    model = Mailer
    extra = 1


class NicknameInline(admin.StackedInline):
    model = Nickname
    extra = 1


class NoteInline(admin.StackedInline):
    model = Note
    extra = 1


# class PhotoInline(admin.StackedInline):
#    model = vcard.models.Photo
#    extra = 1


class RoleInline(admin.StackedInline):
    model = Role
    extra = 1


# class SoundInline(admin.StackedInline):
#    model = Sound
#    extra = 1


class TitleInline(admin.StackedInline):
    model = Title
    extra = 1


class TzInline(admin.StackedInline):
    model = Tz
    extra = 1


class UrlInline(admin.StackedInline):
    model = Url
    extra = 1

def to_vcf_file(modeladmin, request, queryset):
    return vcf_file_view( request, queryset )

to_vcf_file.short_description = "Create vcf file with marked objects"



class ContactAdmin(admin.ModelAdmin):
    
    actions = [ to_vcf_file ]
    
    # list_display = ( 'selectVCFLink' )

    fields = ['fn', 'family_name', 'given_name', 'additional_name', 'honorific_prefix', 'honorific_suffix', 'bday', 'classP']
    inlines = [TelInline, EmailInline, AdrInline, TitleInline, OrgInline, AgentInline, CategoriesInline, KeyInline, LabelInline, NicknameInline, MailerInline, NoteInline, RoleInline, TzInline, UrlInline, GeoInline]
    
    def get_urls(self):
        urls = super(ContactAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^selectVCF/confirmVCF/uploadVCF/$', self.admin_site.admin_view( self.uploadVCF ) ),
            (r'^selectVCF/confirmVCF/$', self.admin_site.admin_view( self.confirmVCF ) ),
            (r'^selectVCF/$', self.admin_site.admin_view( self.selectVCF ) )
        )
        return my_urls + urls

    def uploadVCF( self, request ):
        """ TODO: Docstring """

        if( not request.REQUEST.has_key( 'confirm' ) ):
            return HttpResponseRedirect( '/admin/vcard/contact' )


	newContactList = request.session[ 'unconfirmedContacts' ]

        for i in newContactList :

            i.commit()

        return HttpResponseRedirect( '/admin/vcard/contact' )

    def confirmVCF( self, request ):

        newContactList = []

        for o in vobject.readComponents( request.FILES[ 'upfile' ] ):

            c = Contact.importFrom( "vObject", o ) 

                newContactList.append( c )

        """
        try:
            for o in vobject.readComponents( request.FILES[ 'upfile' ] ):

                c = Contact.importFrom( "vObject", o ) 

                newContactList.append( c )

        except Exception as e:
            print type(e)
            print e.args
            print e
            # for i in newContactList :

            #    i.delete()

            return render_to_response( 'admin/errorVCF.html', {'exception': e }, context_instance=RequestContext(request) )
        """
	request.session[ 'unconfirmedContacts' ] = newContactList

        return render_to_response( 'admin/confirmVCF.html', {'contactSet': newContactList }, context_instance=RequestContext(request) )



    def selectVCFLink( self ):
        """ TODO: Docstring """

        return '<a href="../newsletter/%s/">%s</a>' % (obj.newsletter.id, obj.newsletter)
    selectVCFLink.short_description = _('Select VCF')
    selectVCFLink.allow_tags = True 

    def selectVCF( self, request ):
        """ TODO: Docstring """

        return render_to_response( 'admin/selectVCF.html', context_instance=RequestContext(request) )
        

admin.site.register(Contact, ContactAdmin)
