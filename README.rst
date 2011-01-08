Overview
----------

This document briefly describes installation, dependencies and use of django-vcard.

The django-vcard library offers;

    Contact

        A Django Model for representing vCards
        A Contact can be imported and exported to and from both vCard strings and vobjects

Install
-------

    Just type the following in the commandline:
    
        ``pip install -e -e git+http://github.com/guidocalvano/django-vcard.git#egg=django-vcard``

Dependencies
-------------
 
vObject 

       documentation at http://vobject.skyhouseconsulting.com/ 

       download at http://pypi.python.org/pypi/vobject

Use
---


Create a new Contact object;

``c = Contact()``

Import data into the Contact c;

``c.importFrom( type, data )``

Export data from the Contact 

``exportedData = c.exportTo( type )``

Type is a string describing the type of the data imported or exported.

Valid type strings are;


``"vCard"``   - a vCard string

``"vObject"`` - a vObject containing vCard data

