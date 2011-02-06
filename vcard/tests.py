"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import logging, os

from django.test import TestCase
from vcard.models import Contact

PATH_TO_MODELS_PY = os.path.dirname(os.path.realpath(__file__))


class TestContact(TestCase):
    
    def setUp(self):
        path =     os.path.join( PATH_TO_MODELS_PY, 'testdata' )
        os.chdir(path)
        self.testfiles =  os.listdir(path)
    
    def privateTestString( self, vCard ) :
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
        a = Contact.importFrom( 'vCard', vCard ) 
        
	a.commit()

        b = Contact.importFrom( 'vCard', a.exportTo( 'vCard' ) ) 

        b.commit()

        self.compare_contacts(a, b)
    
    def compare_contacts( self, a, b):
        """ Compares two Contact objects. """
        
        self.assertEqual( a.exportTo( 'vCard' ), b.exportTo( 'vCard' ) )
        
    
    def test_importfiles( self ) :
        """ 
        testing is done by taking all files in a given directory, that are assumed to be 
        just vCards and then testing whether the contained string successfully passes
        testString
        
        """
        
        
        for filename in self.testfiles :
            logging.debug('Importing file %s', filename)
            
            f = open(filename)
            filedata = f.read()

            self.privateTestString( filedata ) 
            
    def test_exportfiles(self):
        """ 
        See whether we can import and then export some files. 
        
        The procedure is as follows:
        1. Open a vCard file
        2. Import the data
        3. Export the data to a string
        4. Write it back to a file
        5. Read it back in
        6. Compare with the original data read in
        7. Compare with to original read contents
        """
        
        for filename in self.testfiles :
            logging.debug('Importing file %s', filename)
            
            f = open(filename)
            filedata1 = f.read()
            
            c1 = Contact.importFrom('vCard', filedata1)
            
            c1.commit()

            f2 = os.tmpfile()
            f2.write(c1.exportTo('vCard'))
            
            f2.seek(0)
            
            filedata2 = f2.read()
            c2 = Contact.importFrom('vCard', filedata2)

            c2.commit()
            
            self.compare_contacts(c1, c2)
            self.assertEqual(filedata1, filedata2)
      
            
        
