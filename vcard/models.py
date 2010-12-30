from django.db import models
import os

# Create your models here.

class Contact( models.Model ) :
    """    
    import export functionality is done via vobject
    
    vobject is not the greatest lib in the world, but its on python.org
    it's poorly documented; had to find some functions using introspection... such as accessing plural properties...
    
    properties of vobject are probably best iterated using getChildren()
         then you check what type of property type and store it in the right place
    
    
    a fundamental queation is naming; 
        do I pick sensible full names, making the code more readable
        do I use the vCard names, making it easier to realte the code to the original vCard
    """
    
    # BUG: This would prevents this model from ever being created
    # from anything else than a string. Perhaps you want something like
    # vCardString=None.
    def __init__( self, vCardString ) :
        
        self.fromString( vCardString )
    
    def __unicode__(self):
        return self.n
    
    # functionality

    
    def fromVObject( vObject ) :
        """
        
        """
        properties = vObject.getChildren()
        
        childModels = []
        
        for property in properties :
            
            if( property.name.upper() == "FN" ) :
                  
                  fn = property.value
            
            if( property.name.upper() == "FN" ) :
                  
                  n = N()

                  childModels.append( n ) 

            
            if( property.name.upper() == "TEL" ) :
                  t = Tel()

                  childModels.append( t ) 

             # etc.
        
        # commit everything
        
        self.save()
        
        for m in childModels :
             m.save()
    
    # NOTE: Not sure if we want this feature.
    def fromString( vCardString ) :
        
        vObject = vobject.readOne( vCardString ) 
        
        fromVObject( vObject )
    
    def toVObject() :
        
        vObject = vobject.vCard() 
        
        vObject.add('n')
        
        # etc.
        
        return vObject
    
    def toString() :
        
        return toVObject().serialize() 
    
    # tests
    
    def __eq__(self, other) : 			# this should compare the objects for equality
        return self.__dict__ == other.__dict__
    
    # BUG: Syntax error. Also, put this in `tests.py`, where it belongs.
    def testString( vCard )
        """
        Rather than making sure import export goes correctly 
        by checking to see whether the resulting string is regenerated,
        the string is used to create a Contact object
        This object recreates the string and that string is used to create another object.
        These objects are then compared.
        The advantage is that comparing two objects is much easier than two strings
        as string can contain for instance arbitrary sequences of whitespaces,
        where each arbitrary sequence of whitespaces obviously equals any other sequence of
        whitespaces.
        """
        a = Contact( vCard )
        b = Contact( a.toString() ) 
        
        return a == b 
    
    def testVCardsInDirectory( self, path )
        """ 
        testing is done by taking all files in a given directory, that are assumed to be 
        just vCards and then testing whether the contained string successfully passes
        testString
        
        """
        fileList = listdir( path )
        
        correct = True
        
        for file in fileList :
            
            str = fopen( file ).read()
            
            correct = correct AND self.testString( str ) 
            if( NOT correct ) return False
    
        return True
    
    # required
    
    # NOTE: Make sure the code is Python PEP8 compliant, for readability.
    # http://pypi.python.org/pypi/pep8
    
    fn     = models.CharField( max_length=1024, unique = True, blank = False, null=False verbose_name = "Formatted Name", help_text = "The formatted name string associated with the vCard object" )   # 1
    n      = models.OneToOneField( N, unique = True, blank = False, null = False, verbose_name="Name", help_text="A structured representation of the name of the person, place or thing associated with the vCard object." ) 
    
    bday   = models.DateField( blank = True, null=True )

    classP        = models.CharField( max_length = 256, blank = True, null=True, verbose_name = "Class" )
    rev           = models.CharField( max_length = 256, blank = True, null=True, verbose_name = "Last Revision" )
    sort_string   = models.CharField( max_length = 256, blank = True, null=True, verbose_name = "Sort String"	 )
    tz            = models.CharField( max_length = 256, blank = True, null=True, verbose_name = "Time Zone" )
    uid           = models.CharField( max_length = 256, blank = True, null=True, verbose_name = "Unique Identifier" )
    
    geo    = models.OneToOneField( Geo, unique = blank = True, null = True )
"""    
V    n # 1 -> TABLE with (family-name, given-name, additional-name, honorific-prefix, honorific-suffix)
    
    # optional, singular
    
V    bday # 0..1
V    class # 0..1
V    rev # 0..1
V    sort-string # 0..1
V    tz # 0..1
V    uid # 0..1
V    geo # 0..1 -> TABLE (latitude, longitude)
    
    # optional plural ALL TABLES

 V   email # * (type, value)
V    adr # * (post-office-box, extended-address, street-address, locality, region, postal-code, country-name, type, value)
    agent # *
    category # *
    key # *
    label # *
    logo # *
    mailer # *
    nickname # *
    note # *
V    org # * (organization-name, organization-unit)
    photo # *
    role # *
    sound # *
V    tel # * (type, value)
    title # *
    url # *
"""

class N( models.Model )
    
    contact = models.ForeignKey( Contact, primary_key = True )
    
    family_name      = models.CharField( max_length = 1024, verbose_name = "Family Name" )
    given_name       = models.CharField( max_length = 1024, verbose_name = "Given Name" )
    aditional_name   = models.CharField( max_length = 1024, verbose_name = "Additional Name" )
    honorific_prefix = models.CharField( max_length = 1024, verbose_name = "Honorific Prefix" )
    honorific_suffix = models.CharField( max_length = 1024, verbose_name = "Honorific Suffix" )

# BUG: Syntax error. Forgot the :'s.
# Also, make sure eache class has a docstring telling what is represents
class Tel( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    type  = models.CharField( max_length=30, verbose_name="type of phone number", help_text="for instance WORK or HOME" )
    value = models.CharField( max_length=100 )
 


class Email( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    type  = models.CharField( max_length=30, verbose_name="type of email" )
    value = models.CharField( max_length=100 )
 



class Geo( models.Model )
    
    contact = models.ForeignKey( Contact, primary_key = True )
    
    latitude      = models.CharField( max_length = 1024, verbose_name = "Latitude" )
    longitude     = models.CharField( max_length = 1024, verbose_name = "Longitude" )




class Org( models.Model )
    
    contact = models.ForeignKey( Contact, primary_key = True )
    
    organization_name     = models.CharField( max_length = 1024, verbose_name = "Organisation name" )
    organization_unit     = models.CharField( max_length = 1024, verbose_name = "Organistion unit" )


class Addr( models.Model )
    
    contact = models.ForeignKey( Contact, primary_key = True )
    
    post_office_box      = models.CharField( max_length = 1024, verbose_name = "Post Office Box" )
    extended_address     = models.CharField( max_length = 1024, verbose_name = "Extended Address" )
    street_address       = models.CharField( max_length = 1024, verbose_name = "Street Address" )
    locality             = models.CharField( max_length = 1024, verbose_name = "Locality" )
    region               = models.CharField( max_length = 1024, verbose_name = "Region" )
    postal_code          = models.CharField( max_length = 1024, verbose_name = "Postal Code" )
    country_name         = models.CharField( max_length = 1024, verbose_name = "Country Name" )
    type                 = models.CharField( max_length = 1024, verbose_name = "Type" )
    value                = models.CharField( max_length = 1024, verbose_name = "Value" )


class Agent( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )



class Category( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )



class Key( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )



class Label( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )


class Agent( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )



class Logo( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )



class Mailer( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )



class Nickname( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )


class Note( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )

class Photo( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )


class Role( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )




class Sound( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )

class Title( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )


class Url( models.model )
    
    contact = models.ForeignKey( Contact, primary_key=True )
    
    data = models.CharField( max_length=100 )






