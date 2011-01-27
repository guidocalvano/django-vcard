"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from vCard.models import *

PATH_TO_MODELS_PY = os.path.dirname(os.path.realpath(__file__))


class TestContact(unittest.TestCase):
    
    def setUp(self):
        return
    
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
        a = Contact()
        a.importFrom( 'vCard', vCard ) 
        
        b = Contact()
        b.importFrom( 'vCard', a.exportTo( 'vCard' ) ) 
         
        self.assertTrue( a.exportTo( 'vCard' ) == b.exportTo( 'vCard' ) )
    
    def test_vCardsInDirectory( self ) :
        """ 
        testing is done by taking all files in a given directory, that are assumed to be 
        just vCards and then testing whether the contained string successfully passes
        testString
        
        """
        path =     os.path.join( PATH_TO_MODELS_PY,'tests' )
        fileList = listdir( path )
        
        correct = True
        
        for file in fileList :
            if( not file[0] == '.' ) : # if the file is not a hidden system file
                str = fdopen( open( os.path.join( path, file ), 0 ) ).read()
                
                self.privateTestString( str ) 
            

if __name__ == '__main__':
    unittest.main()
