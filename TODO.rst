TODO
====

Please translate to English:

Tasks
------
1.  Naar nieuwe git repo **done**
2.  Date issue (see bday at issue 18)
3.  org issue -> kijkt mathijs nog naar **done (orgname and org unit were fine right?)**
4.  geïnternationaliseerde (zie Django docs) verbose_name geeft **done**
5.  django-extensions graph_models **done**
6.  admin interface **done**
7.  inline admin for many (one right?) tomany **done**
8.  view in admin voor uploaden vcard **done**
9.  AGPL
10. Finish setup **done**
    opzet file, moet nog testen, admin houd ik ook nog geen rekening mee 
11. README.rst (reStructuredText) **done**
12. convertTo  **done**
    gedaan als importFrom and exportTo
13. gitignore **done**
14. pep8 **done? will probably have issues again, will look at it tomorrow** 
    gebruikte commando om whitespace om id's toe te staan;
    `pep8 -r --count --ignore=E201,E202,E221,E251 django_vcard.py`
15. Remove application files in root directory (`manage.py`, `urls.py`, `templates`, `*.pyc`, etc.) **done**
16. Unittests from `vcard/models.py` to `vcard/tests/__init__.py` **done**
17. Sensible data types for (at least):
    
    * URL (URLField) **done**
    * Timezone (int, I believe - see what vobject returns) Can be any value, even 'amsterdam' so just used charfield  **done**
    * Photo, Sound, Logo (blob/binary field?) Can be both file and uri with complex specs. Requires both consideration and more time
    * Note (TextField) **done**
    * Address, email and tel type (ChoiceField) You could use a choice field, but specs allow any value 
    * Geo (maybe Lat/lon. - otherwise leave as a string) **done** (left as string, specs are complex)
    * Email (EmailField) **done**
    * Bday (DateField) DateField does not comply to the specs of vcard; "koninginnedag" is a legal value
    * Rev (Integer, maybe? used datefield) **done** BUT could lead to issues; rev is a timestamp but multiple formats exist 
18. Docstrings for at least all the models, and some of the main functions. **done**
    From the docstring the following things should roughly be clear:
    
    1. What does the function do (semantically, not algorithmically)
       
       Something like: "It eats bananas." 
       
       NOT: "It uses enzymes do digest such and such carbonhydrates etc. etc."
    2. What does it return (if it returns anything at all).
    3. What the meaning of eventual parameters are, especially if they're not
       downright evident.

