Django-addressbook example
--------------------------

Features
-----------

* Allow users to register themselves via their Facebook, Twitter,
Google, or OpenID credentials
* Users can create contact records organized into user-defined contact groups
* The app supports storing for each contact:
** Multiple physical addresses
** Multiple phone numbers
** Multiple emails
* Each contact record supports exporting that record in vCard
format (`http://en.wikipedia.org/wiki/VCard`)
* Each contact record presents a QR code to allow a barcode
scanner to import it
* Each contact record accesses any Gravatar for the contact
(`http://en.gravatar.com/`)
* Each contact uses the hCard microformat in its markup
`http://microformats.org/wiki/hcard`
* A full unit test suite
* The app is installable using standard Python distutils

Installing the example 
----------------------

    virtualenv usr
    source usr/bin/activate
    pip install -r requirements.txt

Starting the example
----------------------

    python manage.py runserver 0:8000

