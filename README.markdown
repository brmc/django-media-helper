## django-media-helper

This app is broken into 2 parts.

First, this is a fork of django-cleanup, an app that deletes files from the server when the
associated field or model is changed or deleted. Django-media-helper retains its complete 
functionality.

Now, the new part is that when you upload an image, `media-helper` will automatically resize the image for you
and deliver the most appropriately sized image to the browser. And of course it removes the
images on change or deletion.

From the django-cleanup docs:

**Warning! If you use transactions you may lose you files if transaction will rollback. 
If you are concerned about it you need other solution for old file deletion in your project.**

Most django projects I've seen don't use transactions and this app is designed for such projects.

## How does it work?

django-cleanup connects pre_save and post_delete signals to special functions(these functions 
delete old files) for each model which app is listed in INSTALLED_APPS above than 'django_cleanup'.

## Requirements

This app uses `Pillow` for image resizing.  If you've never used PIL or Pillow before, aside from
the base package itself, you're going to need to make sure you have the appropriate development packages
for image encoding.  **IMPORTANT:  PIL/PIllow WILL 'successfully' install without the encoding
packages, but you won't be able to do much, so you need to install these packages BEFORE you
try to install Pillow.**

The Ajax call to set a session variable uses `Jquery`.

For example, on a Debian-based system, the packages for JPEG's and PNG's are

    libjpeg8-dev libpng12-dev ,

respectively.  And I believe on RPM systems, the only difference is "dev" becomes "devel."  Whatever 
you're using, you will have to do something similar.  

And don't worry, Pillow pisses everyone off at some point.


## Installation
    
    pip install git+git://

Add media_helper to settings.py

    INSTALLED_APPS = (
        ...
        'media_helper', # should go after your apps
    )

**media_helper** should be placed after all your apps. (At least after those apps which need to remove files.)


The following urls are needed to set the session variable to track the resolution.Add the following to 
your root `urls.py`

    urlpatterns = patterns('',
        ...
        url(r'^media-helper/', include('media_helper.urls')),
        ...
    )

We need the resizer.js file to set a session variable.  Of course you don't need this.  Feel free to set the
variable anyway you wish. So let's collect the staticcfiles:

    ./manage.py collectstatic

If you're going to be using the template tag to deliver the new images, remember to restart yourserver after installing the package.

## Usage

The resizing and cleanup functions are done automatically.  Whenever an image is uploaded, changed, or deleted, the images will be 
resized or deleted for you.  You don't need to do anything special.  But to integrate the resized images into your templates, you first need to add the JS source file.  Remember to add this after Jquery:

    {% static 'media-helper/resizer.js' %}

Now when you want to use a resized image, just use the `resolution` filter on an image in the `src` attribute in the `img` tag:

    <img src="{{image|resolution}}" />

And that's it! Well, except for the other stuff...

## Configuration


