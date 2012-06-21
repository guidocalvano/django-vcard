import logging, os
import datetime
from datetime import *

from django.test import TestCase
from vcard.models import Contact

PATH_TO_MODELS_PY = os.path.dirname(os.path.realpath(__file__))


class TestContact(TestCase):

    def setUp(self):
        self.path = os.path.join(PATH_TO_MODELS_PY, 'testdata')

        os.chdir(self.path)
        self.testfiles = os.listdir(self.path)

    def privateTestString(self, vCard):
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
        a = Contact.importFrom('vCard', vCard)

        a.commit()

        b = Contact.importFrom('vCard', a.exportTo('vCard'))

        b.commit()

        self.compare_contacts(a, b)

    def compare_contacts(self, a, b):
        """ Compares two Contact objects. """
        self.assertEqual(a.exportTo('vCard'), b.exportTo('vCard'))

    def test_importfiles(self):
        """
        testing is done by taking all files in a given directory, that are assumed to be
        just vCards and then testing whether the contained string successfully passes
        testString
        """

        for filename in self.testfiles :
            logging.debug('Importing file %s', filename)

            f = open(filename)
            filedata = f.read()

            self.privateTestString(filedata)

    def test_all_properties_imported_and_exported(self):

        testVcard = "BEGIN:VCARD\n\
VERSION:3.0\n\
FN:Forrest Gump\n\
N:family_name;given_name;additional_name;honorific_prefix;honorific_suffix\n\
ADR;TYPE=WORK:post_office_box;extended_address;street_address;locality;region;postal_code;country\n\
AGENT:agent\n\
BDAY;value=date:2001-01-04\n\
CATEGORIES:category\n\
CLASS:class\n\
EMAIL;TYPE=PREF:forrestgump@example.com\n\
GEO:geo\n\
KEY:key\n\
LABEL:label\n\
NICKNAME:nickname\n\
NOTE:note\n\
ORG:ABC;North American Division\n\
REV:20080424T195243Z\n\
ROLE:role\n\
SORT-STRING:sort_string\n\
TEL;TYPE=WORK:(111) 555-1212\n\
TITLE:Shrimp Man\n\
TZ:tz\n\
UID:uid\n\
URL:http://www.google.com\n\
END:VCARD\n"

        all = Contact.importFrom('vCard', testVcard)

        all.commit()

        self.assertEqual(all.fn, "Forrest Gump")

        self.assertEqual(all.family_name, "family_name")
        self.assertEqual(all.given_name, "given_name")
        self.assertEqual(all.additional_name, "additional_name")
        self.assertEqual(all.honorific_prefix, "honorific_prefix")
        self.assertEqual(all.honorific_suffix, "honorific_suffix")

        ad = all.adr_set.all()[0]

        self.assertEqual(ad.post_office_box, "post_office_box")
        self.assertEqual(ad.extended_address, "extended_address")
        self.assertEqual(ad.street_address, "street_address")
        self.assertEqual(ad.locality, "locality")
        self.assertEqual(ad.region, "region")
        self.assertEqual(ad.postal_code, "postal_code")
        self.assertEqual(ad.type, "WORK")

        self.assertEqual(all.agent_set.all()[0].data, "agent")

        self.assertEqual(all.bday, date(2001, 1, 4))

        self.assertEqual(all.category_set.all()[0].data, "category")
        self.assertEqual(all.classP, "class")

        self.assertEqual(all.email_set.all()[0].type,  "PREF")
        self.assertEqual(all.email_set.all()[0].value,  "forrestgump@example.com")
        self.assertEqual(all.geo_set.all()[0].data,  u'geo')
        self.assertEqual(all.key_set.all()[0].data,  u'key')
        self.assertEqual(all.label_set.all()[0].data,  u'label')
        self.assertEqual(all.nickname_set.all()[0].data,  u'nickname')
        self.assertEqual(all.note_set.all()[0].data,  u'note')

        self.assertEqual(all.org_set.all()[0].organization_name,  u"ABC")
        self.assertEqual(all.org_set.all()[0].organization_unit,  u'North American Division')

        self.assertEqual(all.rev, datetime(1970, 8, 21, 4, 53, 44))

        self.assertEqual(all.role_set.all()[0].data, u'role')
        self.assertEqual(all.sort_string, u'sort_string')

        self.assertEqual(all.tel_set.all()[0].value, u'(111) 555-1212')
        self.assertEqual(all.tel_set.all()[0].type, u'WORK')

        self.assertEqual(all.title_set.all()[0].data, "Shrimp Man")
        self.assertEqual(all.tz_set.all()[0].data, "tz")

        self.assertEqual(all.uid, "uid")
        self.assertEqual(all.url_set.all()[0].data, "http://www.google.com")

    def off_test_exportfiles(self):
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
