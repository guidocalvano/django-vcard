from django.db import models
import os
from os import *
import vobject
from vobject.vcard import *
from django.utils.translation import ugettext as _
import time
import datetime
from datetime import *
from time import *
import re

class Contact(models.Model):
    """
    import export functionality is done via vobject

    vobject is not the greatest lib in the world, but its on python.org
    it's poorly documented; had to find some functions using introspection...
    such as accessing plural properties...

    properties of vobject are probably best iterated using getChildren()
         then you check what type of property type and store it in the
         right place


    a fundamental queation is naming;
        do I pick sensible full names, making the code more readable
        do I use the vCard names, making it easier to relate the code to
        the original vCard
    """
    def __unicode__(self):
        return self.fn


    class Meta:
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")

    # functionality
    def importFrom( self, type, data ):
        """
	The contact sets its properties as specified in the argument 'data'
        according to the specification given in the string passed as 
        argument 'type'

        'type' can be either 'vCard' or 'vObject'

        'vCard' is a string containing containing contact information
        formatted according to the vCard specification

        'vObject' is a vobject containing vcard contact information 
        """
        if( type == "vCard" ):
            self.fromVCard( data )
            return

        if( type == "vObject" ):
            self.fromVObject( data )
            return

    def exportTo( self, type ):
        """
	The contact returns an object with its properties in a format as 
        defined by the argument type.

        'type' can be either 'vCard' or 'vObject'

        'vCard' is a string containing containing contact information
        formatted according to the vCard specification

        'vObject' is a vobject containing vcard contact information 
        """
        if( type == "vCard" ):
            return self.toVCard()

        if( type == "vObject" ):
            return self.toVObject()

    def fromVObject( self, vObject ):
        """
        Contact sets its properties as specified by the supplied
        vObject.
        """
        properties = vObject.getChildren()

        childModels = []

        fnFound = False
        nFound = False

        for property in properties:
            # ----------- REQUIRED PROPERTIES --------------
            if( property.name.upper() == "FN" ):

                fnFound = True

                self.fn = property.value

            if( property.name.upper() == "N" ):

                nFound = True

                # nObject = N()

                # nObject.contact = self

                family_name = property.value.family
                given_name = property.value.given
                additional_name = property.value.additional
                honorific_prefix = property.value.prefix
                honorific_suffix = property.value.suffix

                # childModels.append( nObject )

            # ----------- OPTIONAL MULTIPLE VALUE TABLE PROPERTIES -------
            """

            """
            if( property.name.upper() == "TEL" ):

                t = Tel()

                t.contact = self

                for key in property.params.iterkeys():
                    if( key.upper() == "TYPE" ):
                        t.type = property.params[ key ][ 0 ]

                t.value = property.value

                childModels.append( t )

            if( property.name.upper() == "ADR" ):
                adr = Adr()

                adr.contact = self

                adr.post_office_box = property.value.box
                adr.extended_address = property.value.extended
                adr.street_address = property.value.street
                adr.locality = property.value.city
                adr.region = property.value.region
                adr.postal_code = property.value.code
                adr.country_name = property.value.country

                for key in property.params.iterkeys():
                    if( key.upper() == "TYPE" ):
                        adr.type = property.params[ key ][ 0 ]
                    # if( key.upper() == "VALUE" ):
                    #    adr.value = property.params[ key ][ 0 ]

                childModels.append( adr )

            if( property.name.upper() == "EMAIL" ):
                email = Email()  # email (type, value)

                email.contact = self

                for key in property.params.iterkeys():
                    if( key.upper() == "TYPE" ):
                        email.type = property.params[ key ][ 0 ]

                email.value = property.value

                childModels.append( email )

            if( property.name.upper() == "ORG" ):
                org = Org()  # org (organization_name, organization_unit)

                org.organization_name = property.value[ 0 ]
                if( len( property.value ) > 1 ):
                    org.organization_unit = property.value[ 1 ]

                childModels.append( org )

            # ---------- OPTIONAL SINGLE VALUE NON TABLE PROPERTIES ---
            # these values can simply be assigned to the member value

            if( property.name.upper() == "BDAY" ):

                year  = int( property.value[0:4] )
                month = int( property.value[4:6] )
                day   = int( property.value[6:8] )

                self.bday = date( year, month, day )

            if( property.name.upper() == "CLASS" ):
                self.classP = property.value

            try: 
                if( property.name.upper() == "REV" ):
                    self.rev = datetime.fromtimestamp( int( re.match( '\\d+', property.value).group( 0 ) ) )
                # do nothing just don't set rev
            except:
                print "did not set rev... not even worth mentioning, but I have to write something"
                
            # note there is still a distinct possibility the timestamp is misread!
            # many formats exist for timestamps, that all have different starting times etc. 
            # supporting rev is in my opinion doomed to fail...

            if( property.name.upper() == "SORT-STRING" ):
                self.sort_string = property.value

            if( property.name.upper() == "UID" ):
                self.uid = property.value

            # ---------- MULTI VALUE NON TABLE PROPERTIES-----------

            if( property.name.upper() == "AGENT" ):

                agent = Agent()
                agent.data = property.value
                childModels.append( agent )

            if( property.name.upper() == "CATEGORIES" ):

                categories = Categories()
                categories.data = property.value

                childModels.append( categories )

            if( property.name.upper() == "GEO" ):
                geo = Geo()
                geo.data = property.value

                childModels.append( geo )

            if( property.name.upper() == "TZ" ):
                tz = Tz()
                tz.data = property.value

                childModels.append( tz )

            if( property.name.upper() == "KEY" ):

                key = Key()
                key.data = property.value

                childModels.append( key )

            if( property.name.upper() == "LABEL" ):

                label = Label()
                label.data = property.value

                childModels.append( label )

            if( property.name.upper() == "MAILER" ):

                mailer = Mailer()
                mailer.data = property.value

                childModels.append( mailer )

            if( property.name.upper() == "NICKNAME" ):

                nickname = Nickname()
                nickname.data = property.value

                childModels.append( nickname )

            if( property.name.upper() == "NOTE" ):

                note = Note()
                note.data = property.value

                childModels.append( note )

            if( property.name.upper() == "PHOTO" ):

                photo = Photo()
                photo.data = property.value

                childModels.append( photo )

            if( property.name.upper() == "ROLE" ):

                role = Role()
                role.data = property.value

                childModels.append( role )

            if( property.name.upper() == "SOUND" ):

                sound = Sound()
                sound.data = property.value

                childModels.append( sound )

            if( property.name.upper() == "TITLE" ):

                title = Title()
                title.data = property.value

                childModels.append( title )

            if( property.name.upper() == "URL" ):

                url = Url()

                # ':' is replaced with '\:' because ':' must be escaped in vCard files 
                url.data = re.sub( r'\\:', ':',  property.value )

                childModels.append( url )

            if( property.name.upper() == "LOGO" ):

                logo = Logo()
                logo.data = property.value

                childModels.append( logo )

        # nObject.save()

        # self.n = nObject
        self.save()

        for m in childModels:
            m.contact = self
            m.save()

    def fromVCard( self, vCardString ):
        """
        Contact sets its properties as specified by the supplied
        string. The string is in vCard format.
        """
        vObject = vobject.readOne( vCardString )

        self.fromVObject( vObject )

    def toVObject( self ):
        """
        returns a cast of the Contact to vobject 
        """
        v = vobject.vCard()

        n = v.add('n')

        n.value = vobject.vcard.Name(
               given = self.given_name,
               family = self.family_name,
               additional = self.additional_name,
               prefix = self.honorific_prefix,
               suffix = self.honorific_suffix )

        fn = v.add('fn')

        fn.value = self.fn

        for j in self.adr_set.all():

            i = v.add( 'adr' )

            jstreet   = j.street_address if j.street_address else ''
            jbox      = j.post_office_box if j.post_office_box else ''
            jregion   = j.region if  j.region else ''
            jcode     = j.postal_code if j.postal_code else ''
            jcountry  = j.country_name if j.country_name else ''
            jextended = j.extended_address if j.extended_address else ''

            i.type_param = j.type
            i.value = vobject.vcard.Address(
                     box = jbox,
                     extended = jextended,
                     street = jstreet,
                     region = jregion,
                     code = jcode,
                     country = jcountry )

        for j in self.org_set.all():
            i = v.add( 'org' )
            i.value[ 0 ]   = j.organization_name
            i.value.append( j.organization_unit )

        for j in self.email_set.all():
            i = v.add( 'email' )
            i.value = j.value
            i.type_param = j.type

        for j in self.tel_set.all():
            i = v.add( 'tel' )
            i.value = j.value
            i.type_param = j.type

        if( self.classP ):
            i = v.add( 'class' )
            i.value = self.classP

        if( self.rev ):
            i = v.add( 'rev' )
            i.value = str( int( mktime( self.rev.timetuple() ) ) )

        if( self.sort_string ):
            i = v.add( 'sort-string' )
            i.value = self.sort_string

        if( self.uid ):
            i = v.add( 'uid' )
            i.value = self.uid

        if( self.bday ):

            i = v.add( 'bday' )

            yearString  = str( self.bday.year )
            monthString = str( self.bday.month )
            dayString   = str( self.bday.day )

            if( len( monthString ) == 1 ): monthString = '0' + monthString
            if( len( dayString   ) == 1 ): dayString = '0' + dayString
            i.value = yearString + monthString + dayString

        for j in self.geo_set.all():
            i = v.add( 'geo' )
            i.value = j.data

        for j in self.tz_set.all():
            i = v.add( 'tz' )
            i.value = j.data

        for j in self.agent_set.all():
            i = v.add('agent' )
            i.value = j.data

        for j in self.categories_set.all():
            i = v.add('categories' )
            i.value = j.data

        for j in self.key_set.all():
            i = v.add('key' )
            i.value = j.data

        for j in self.label_set.all():
            i = v.add('label' )
            i.value = j.data

        #        for j in self.logo_set.all():
        #            i = v.add('logo' )
        #            i.value = j.data

        for j in self.mailer_set.all():
            i = v.add('mailer' )
            i.value = j.data

        for j in self.nickname_set.all():
            i = v.add('nickname' )
            i.value = j.data

        for j in self.note_set.all():
            i = v.add('note' )
            i.value = j.data

        #        for j in self.photo_set.all():
        #            i = v.add('photo' )
        #            i.value = j.data

        for j in self.role_set.all():
            i = v.add('role' )
            i.value = j.data

        #        for j in self.sound_set.all():
        #            i = v.add('sound' )
        #            i.value = j.data

        for j in self.title_set.all():
            i = v.add('title' )
            i.value = j.data

        for j in self.url_set.all():
            i = v.add('url' )
            i.value = j.data

        return v

    def toVCard( self):
        """
        returns a cast of the Contact to a string in vCard format. 
        """
        return self.toVObject().serialize()

    # primary key

    id = models.AutoField(primary_key=True)

    # required

    fn = models.CharField(
     max_length=1024,
     blank = False,
     null=False,
     verbose_name = _("formatted name"),
     help_text = _("The formatted name string associated with the vCard object" ) )

    family_name      = models.CharField( max_length = 1024,
                                         verbose_name = _( "family name" ))
    given_name       = models.CharField( max_length = 1024,
                                         verbose_name = _("given name" ))
    additional_name   = models.CharField( max_length = 1024,
                                          verbose_name = _("additional name" ))
    honorific_prefix = models.CharField( max_length = 1024,
                                         verbose_name = _("honorific prefix" ))
    honorific_suffix = models.CharField( max_length = 1024,
                                         verbose_name = _("honorific suffix" ))

    # n = models.OneToOneField( 'N',
    #    unique = True,
    #    blank = False,
    #    null = False,
    #    verbose_name=_("Name"),
    #    help_text=_("A structured representation \
    # of the name of the person, place or \
    # thing associated with the vCard object.") )


    # bday can be formulated in various ways
    # some ways are dates, but according 
    # to the vcard specs 'koninginnendag'
    # is perfectly fine. That is why bday
    # is stored as a CharField
    bday   = models.DateField(
       blank = True,
       null=True,
       verbose_name = _("birthday" ) )

    classP        = models.CharField(
       max_length = 256,
       blank = True,
       null=True,
       verbose_name = _("class" ) )

    rev           = models.DateTimeField(
       blank = True,
       null=True,
       verbose_name = _("last revision" ) )

    sort_string   = models.CharField(
       max_length = 256,
       blank = True,
       null=True,
       verbose_name = _("sort string") )

    # a uid is a URI. A URI consists of both
    # a URL and a URN. So using a URLField is 
    # incorrect. Given that no URIField is available
    # a common CharField was used
    uid           = models.CharField(
       max_length = 256,
       blank = True,
       null=True,
       verbose_name = _("unique identifier" ) )

"""
class N( models.Model ):
    class Meta:
        verbose_name = _("name")
        verbose_name_plural = _("names")

    contact = models.ForeignKey( Contact, unique=True )

    family_name      = models.CharField( max_length = 1024,
                                         verbose_name = _( "Family Name" ))
    given_name       = models.CharField( max_length = 1024,
                                         verbose_name = _("Given Name" ))
    additional_name   = models.CharField( max_length = 1024,
                                          verbose_name = _("Additional Name" ))
    honorific_prefix = models.CharField( max_length = 1024,
                                         verbose_name = _("Honorific Prefix" ))
    honorific_suffix = models.CharField( max_length = 1024,
                                         verbose_name = _("Honorific Suffix" ))

    def __unicode__( self ):
        return '' + self.given_name + ' ' + self.family_name
"""

class Tel( models.Model ):
    """
    A telephone number of a contact
    """

    class Meta:
        verbose_name = _("telephone number")
        verbose_name_plural = _("telephone numbers")

    TYPE_CHOICES = (
        ('VOICE', _(u"INTL")),
        ('HOME', _(u"home")),
        ('MSG',  _(u"message")),
        ('WORK',  _(u"work")),
        ('pref',  _(u"prefered")),
        ('fax',  _(u"fax")),
        ('cell',  _(u"cell phone")),
        ('video',  _(u"video")),
        ('pager',  _(u"pager")),
        ('bbs',  _(u"bbs")),
        ('modem',  _(u"modem")),
        ('car',  _(u"car phone")),
        ('isdn',  _(u"isdn")),
        ('pcs',  _(u"pcs")),
    )

    contact = models.ForeignKey( Contact )

    # making a choice field of type is incorrect as arbitrary
    # types of phone number are allowed by the vcard specs.
    type  = models.CharField( max_length=30,
                              verbose_name=_("type of phone number"),
                              help_text=_("for instance WORK or HOME" ), choices=TYPE_CHOICES)
    value = models.CharField( max_length=100, 
                              verbose_name=_("value") )


class Email( models.Model ):
    """
    An email of a contact
    """
    class Meta:
        verbose_name = _("email")
        verbose_name_plural = _("emails")

    TYPE_CHOICES = (
        ('INTERNET', _(u"internet")),
        ('x400', _(u"x400")),
        ('pref', _(u"pref")),
    )

    contact = models.ForeignKey( Contact )

    type  = models.CharField( max_length=30,
                              verbose_name=_("type of email"), choices=TYPE_CHOICES)
    value = models.EmailField( max_length=100, 
                              verbose_name=_("value") )

class Geo( models.Model ):
    """
    A geographical location associated with the contact
    in geo uri format
    """
    class Meta:
        verbose_name = _("geographic uri")
        verbose_name_plural = _("geographic uri's")

    contact = models.ForeignKey( Contact )

    # because vobject can't properly pass the geo uri for now the
    # field is specified as a normal CharField
    data      = models.CharField( max_length = 1024,
                                  verbose_name = _("geographic uri" ))


class Org( models.Model ):
    """
    An organization and unit the contact is affiliated with.
    """
    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    contact = models.ForeignKey( Contact )

    organization_name     = models.CharField( max_length = 1024,
                                      verbose_name = _("organization name" ))
    organization_unit     = models.CharField( max_length = 1024,
                                      verbose_name = _("organization unit" ))


class Adr( models.Model ):
    """
    An address
    """
    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    TYPE_CHOICES = (
        ('INTL', _(u"INTL")),
        ('POSTAL', _(u"postal")),
        ('PARCEL',  _(u"parcel")),
        ('WORK',  _(u"work")),
        ('dom',  _(u"dom")),
        ('home',  _(u"home")),
        ('pref',  _(u"pref")),
    )

    contact = models.ForeignKey( Contact )

    post_office_box      = models.CharField( max_length = 1024,
                                             verbose_name = _("post office box" ))
    extended_address     = models.CharField( max_length = 1024,
                                             verbose_name = _("extended address"))
    street_address       = models.CharField( max_length = 1024,
                                             verbose_name = _("street address" ))
    locality             = models.CharField( max_length = 1024,
                                             verbose_name = _("locality"))
    region               = models.CharField( max_length = 1024,
                                             verbose_name = _("region"))
    postal_code          = models.CharField( max_length = 1024,
                                             verbose_name = _("postal code"))
    country_name         = models.CharField( max_length = 1024,
                                             verbose_name = _("country name"))
    type                 = models.CharField( max_length = 1024,
                                             verbose_name = _("type" ), choices=TYPE_CHOICES)
    # value                = models.CharField( max_length = 1024,
    #                                         verbose_name = _("Value"))


class Agent( models.Model ):
    """
    An agent of the contact
    """
    class Meta:
        verbose_name = _("agent")
        verbose_name_plural = _("agents")

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Categories( models.Model ):
    """
    Specifies application category information about the
    contact.  Also known as "tags".    
    """
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Key( models.Model ):
    """
    Specifies a public key or authentication certificate
    associated with the contact information
    """
    class Meta:
        verbose_name = _("key")
        verbose_name_plural = _("keys")

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Label( models.Model ):
    """
    Formatted text corresponding to a delivery
    address of the object the vCard represents
    """
    class Meta:
        verbose_name = _("label")
        verbose_name_plural = _("labels")

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=2000 )


# class Logo( models.Model ):
#    """
#    A logo associated with the contact 

#    The data could be stored in binary or as a uri
#    as could be indicated by a type field

#    My advice; don't. The vcard specs on communicating
#    files are terrible. I'd even leave the entire field
#    out, and wouldn't bother with it. Otherwise it 
#    would take a lot of time!
#    """
#    class Meta:
#        verbose_name = _("logo")
#        verbose_name_plural = _("logos")

#    contact = models.ForeignKey( Contact )

#    data = models.TextField()


class Mailer( models.Model ):
    """
    No longer supported in draft vcard specificiation of July 12 2010
    """
    class Meta:
        verbose_name = _("mailer")
        verbose_name_plural = _("mailers")

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=2000 )


class Nickname( models.Model ):
    """
    The nickname of the
    object the vCard represents.
    """
    class Meta:
        verbose_name = _("nickname")
        verbose_name_plural = _("nicknames")


    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Note( models.Model ):
    """
    Supplemental information or a comment that is
    associated with the vCard.
    """
    class Meta:
        verbose_name = _("note")
        verbose_name_plural = _("notes")


    contact = models.ForeignKey( Contact )

    data = models.TextField()


# class Photo( models.Model ):
#    """
#    A photo of some aspect of the contact 
#
#    The data could be stored in binary or as a uri
#    as could be indicated by a type field

#    My advice; don't. The vcard specs on communicating
#    files are terrible. I'd even leave the entire field
#    out, and wouldn't bother with it. Otherwise it 
#    would take a lot of time!
#    """
#    class Meta:
#        verbose_name = _("photo")
#        verbose_name_plural = _("photos")


#    contact = models.ForeignKey( Contact )

#    data = models.TextField()


class Role( models.Model ):
    """
    The function or part played in a particular
    situation by the object the vCard represents.
    """
    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")


    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


# class Sound( models.Model ):
#    """
#    A sound about some aspect of the contact 

#    The data could be stored in binary or as a uri
#    as could be indicated by a type field

#    My advice; don't. The vcard specs on communicating
#    files are terrible. I'd even leave the entire field
#    out, and wouldn't bother with it. Otherwise it 
#    would take a lot of time!
#    """
#    class Meta:
#        verbose_name = _("sound")
#        verbose_name_plural = _("sounds")
#    contact = models.ForeignKey( Contact )

#    data = models.TextField()


class Title( models.Model ):
    """
    The position or job of the contact
    """
    class Meta:
        verbose_name = _("title")
        verbose_name_plural = _("titles")

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Tz( models.Model ):
    """
    A time zone of a contact

    Tz is represented as a CharField and not in a formal structure because 
    the vcard specification allows city names as tz parameters
    """
    class Meta:
        verbose_name = _("time zone")
        verbose_name_plural = _("time zones")
    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Url( models.Model ):
    """
    A Url associted with a contact.
    """
    class Meta:
        verbose_name = _("url")
        verbose_name_plural = _("url's")
    contact = models.ForeignKey( Contact )

    data = models.URLField( verify_exists=False )
