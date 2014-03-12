Django-addressbook example for Django 1.6
-----------------------------------------

Features
-----------

* Users can create contact records organized into user-defined contact groups
* The app supports storing for each contact: multiple physical addresses, phone numbers and emails
* Each contact record supports exporting that record in vCard format (`http://en.wikipedia.org/wiki/VCard`)
* Each contact record presents a QR code to allow a barcode scanner to import it
* Each contact record displays a Gravatar for the contact, if available (`http://en.gravatar.com/`)
* Each contact uses the hCard microformat in its markup `http://microformats.org/wiki/hcard`
* Allow users to add Social credentials

Installing the app 
----------------------

* Download the branch example 
* pip install -r requirements

Please, consider to use virtualenv in all cases.

NOTES
---------

vCard Format: **http://www.ietf.org/rfc/rfc2426.txt**

Vobject Django snippet: **http://djangosnippets.org/snippets/58/**

Vobject usage: **http://vobject.skyhouseconsulting.com/usage.html, http://lists.brotherharris.com/pipermail/vobject/2009-January/000165.html**
