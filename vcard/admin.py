from vcard.models import *
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from vcard.admin_views import *
import vcard

class NInline(admin.StackedInline):
    model = N
    extra = 1


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


class CategoryInline(admin.StackedInline):
    model = Category
    extra = 1


class KeyInline(admin.StackedInline):
    model = Key
    extra = 1


class LabelInline(admin.StackedInline):
    model = vcard.models.Label
    extra = 1


class LogoInline(admin.StackedInline):
    model = Logo
    extra = 1


class MailerInline(admin.StackedInline):
    model = Mailer
    extra = 1


class NicknameInline(admin.StackedInline):
    model = Nickname
    extra = 1


class NoteInline(admin.StackedInline):
    model = Note
    extra = 1


class PhotoInline(admin.StackedInline):
    model = vcard.models.Photo
    extra = 1


class RoleInline(admin.StackedInline):
    model = Role
    extra = 1


class SoundInline(admin.StackedInline):
    model = Sound
    extra = 1


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
    
    fields = ['fn', 'bday', 'classP', 'rev', 'sort_string','uid']
    inlines = [N,TelInline, EmailInline, AdrInline, TitleInline, OrgInline, AgentInline, CategoryInline, KeyInline, LabelInline,LogoInline, NicknameInline, MailerInline, NoteInline, PhotoInline, RoleInline, SoundInline, TzInline, UrlInline, GeoInline]

admin.site.register(Contact, ContactAdmin)
