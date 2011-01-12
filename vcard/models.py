from django.db import models
import os
from os import *
import vobject
from vobject.vcard import *
import unittest

# Create your models here.


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
        return self.n.__unicode__()

    # functionality
    def importFrom( self, type, data ):
        """

        """
        if( type == "vCard" ):
            self.fromVCard( data )
            return

        if( type == "vObject" ):
            self.fromVObject( data )
            return

    def exportTo( self, type ):
        """

        """
        if( type == "vCard" ):
            return self.toVCard()

        if( type == "vObject" ):
            return self.toVObject()

    def fromVObject( self, vObject ):
        """

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

                nObject = N()

                nObject.family_name = property.value.family
                nObject.given_name = property.value.given
                nObject.additional_name = property.value.additional
                nObject.honorific_prefix = property.value.prefix
                nObject.honorific_suffix = property.value.suffix

                childModels.append( nObject )

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
                    if( key.upper() == "VALUE" ):
                        adr.value = property.params[ key ][ 0 ]

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
                self.bday = property.value

            if( property.name.upper() == "CLASS" ):
                self.classP = property.value

            if( property.name.upper() == "REV" ):
                self.rev = property.value

            if( property.name.upper() == "SORT-STRING" ):
                self.sort_string = property.value

            if( property.name.upper() == "UID" ):
                self.uid = property.value

            # ---------- MULTI VALUE NON TABLE PROPERTIES-----------

            if( property.name.upper() == "AGENT" ):

                agent = Agent()
                agent.data = property.value
                childModels.append( agent )

            if( property.name.upper() == "CATEGORY" ):

                category = Category()
                category.data = property.value

                childModels.append( category )

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
                url.data = property.value

                childModels.append( url )

            if( property.name.upper() == "LOGO" ):

                logo = Logo()
                logo.data = property.value

                childModels.append( logo )

        nObject.save()

        self.n = nObject
        self.save()

        for m in childModels:
            m.contact = self
            m.save()

    def fromVCard( self, vCardString ):

        vObject = vobject.readOne( vCardString )

        self.fromVObject( vObject )

    def toVObject( self ):

        v = vobject.vCard()

        n = v.add('n')

        n.value = vobject.vcard.Name(
               given = self.n.given_name,
               family = self.n.family_name,
               additional = self.n.additional_name,
               prefix = self.n.honorific_prefix,
               suffix = self.n.honorific_suffix )

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
            i.value = self.rev

        if( self.sort_string ):
            i = v.add( 'sort-string' )
            i.value = self.sort_string

        if( self.uid ):
            i = v.add( 'uid' )
            i.value = self.uid

        for j in self.geo_set.all():
            i = v.add( 'geo' )
            i.value = j.data

        for j in self.tz_set.all():
            i = v.add( 'tz' )
            i.value = j.data

        for j in self.agent_set.all():
            i = v.add('agent' )
            i.value = j.data

        for j in self.category_set.all():
            i = v.add('category' )
            i.value = j.data

        for j in self.key_set.all():
            i = v.add('key' )
            i.value = j.data

        for j in self.label_set.all():
            i = v.add('label' )
            i.value = j.data

        for j in self.logo_set.all():
            i = v.add('logo' )
            i.value = j.data

        for j in self.mailer_set.all():
            i = v.add('mailer' )
            i.value = j.data

        for j in self.nickname_set.all():
            i = v.add('nickname' )
            i.value = j.data

        for j in self.note_set.all():
            i = v.add('note' )
            i.value = j.data

        for j in self.photo_set.all():
            i = v.add('photo' )
            i.value = j.data

        for j in self.role_set.all():
            i = v.add('role' )
            i.value = j.data

        for j in self.sound_set.all():
            i = v.add('sound' )
            i.value = j.data

        for j in self.title_set.all():
            i = v.add('title' )
            i.value = j.data

        for j in self.url_set.all():
            i = v.add('url' )
            i.value = j.data

        return v

    def toVCard( self):

        return self.toVObject().serialize()

    # primary key

    id = models.AutoField(primary_key=True)

    # required

    fn = models.CharField(
     max_length=1024,
     blank = False,
     null=False,
     verbose_name = "Formatted Name",
     help_text = "The formatted name string associated with the vCard object" )

    n = models.OneToOneField( 'N',
        unique = True,
        blank = False,
        null = False,
        verbose_name="Name",
        help_text="A structured representation \
of the name of the person, place or \
thing associated with the vCard object." )

    bday   = models.CharField(
       max_length = 256,
       blank = True,
       null=True,
       verbose_name = "Birthday" )

    classP        = models.CharField(
       max_length = 256,
       blank = True,
       null=True,
       verbose_name = "Class" )

    rev           = models.CharField(
       max_length = 256,
       blank = True,
       null=True,
       verbose_name = "Last Revision" )

    sort_string   = models.CharField(
       max_length = 256,
       blank = True,
       null=True,
       verbose_name = "Sort String")

    uid           = models.CharField(
       max_length = 256,
       blank = True,
       null=True,
       verbose_name = "Unique Identifier" )


class N( models.Model ):

    # contact = models.ForeignKey( Contact, primary_key = True )

    family_name      = models.CharField( max_length = 1024,
                                         verbose_name = "Family Name" )
    given_name       = models.CharField( max_length = 1024,
                                         verbose_name = "Given Name" )
    additional_name   = models.CharField( max_length = 1024,
                                          verbose_name = "Additional Name" )
    honorific_prefix = models.CharField( max_length = 1024,
                                         verbose_name = "Honorific Prefix" )
    honorific_suffix = models.CharField( max_length = 1024,
                                         verbose_name = "Honorific Suffix" )

    def __unicode__( self ):
        return '' + self.given_name + ' ' + self.family_name


class Tel( models.Model ):

    contact = models.ForeignKey( Contact )

    type  = models.CharField( max_length=30,
                              verbose_name="type of phone number",
                              help_text="for instance WORK or HOME" )
    value = models.CharField( max_length=100 )


class Email( models.Model ):

    contact = models.ForeignKey( Contact )

    type  = models.CharField( max_length=30,
                              verbose_name="type of email" )
    value = models.CharField( max_length=100 )


class Geo( models.Model ):

    contact = models.ForeignKey( Contact )

    data      = models.CharField( max_length = 1024,
                                  verbose_name = "Geographic uri" )


class Org( models.Model ):

    contact = models.ForeignKey( Contact )

    organization_name     = models.CharField( max_length = 1024,
                                      verbose_name = "Organization name" )
    organization_unit     = models.CharField( max_length = 1024,
                                      verbose_name = "Organization unit" )


class Adr( models.Model ):

    contact = models.ForeignKey( Contact )

    post_office_box      = models.CharField( max_length = 1024,
                                             verbose_name = "Post Office Box" )
    extended_address     = models.CharField( max_length = 1024,
                                             verbose_name = "Extended Address")
    street_address       = models.CharField( max_length = 1024,
                                             verbose_name = "Street Address" )
    locality             = models.CharField( max_length = 1024,
                                             verbose_name = "Locality" )
    region               = models.CharField( max_length = 1024,
                                             verbose_name = "Region" )
    postal_code          = models.CharField( max_length = 1024,
                                             verbose_name = "Postal Code" )
    country_name         = models.CharField( max_length = 1024,
                                             verbose_name = "Country Name" )
    type                 = models.CharField( max_length = 1024,
                                             verbose_name = "Type" )
    value                = models.CharField( max_length = 1024,
                                             verbose_name = "Value" )


class Agent( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Category( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Key( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Label( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Logo( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Mailer( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Nickname( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Note( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Photo( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Role( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Sound( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Title( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Tz( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )


class Url( models.Model ):

    contact = models.ForeignKey( Contact )

    data = models.CharField( max_length=100 )
