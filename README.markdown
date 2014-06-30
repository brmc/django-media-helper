## django-media-helper

This app is broken into 2 parts.

`media_helper.cleanup:`

First, this is a fork of django-cleanup, an app that deletes files from 
the server when the associated field or model is changed or deleted. 
Django-media-helper retains its complete functionality.


`media_helper.resizer`

Now, the new part is that when you upload an image, `media-helper` will 
automatically resize the image for you and deliver the most appropriately 
sized image to the browser. And of course it removes the images on change 
or deletion.

From the django-cleanup docs:

<<<<<<< HEAD
**Warning! If you use transactions you may lose you files if transaction 
will rollback. If you are concerned about it you need other solution for 
old file deletion in your project.**

Most django projects I've seen don't use transactions and this app is 
designed for such projects.
=======

**Warning! If you use transactions you may lose you files if transaction will rollback. 
If you are concerned about it you need other solution for old file deletion in your project.**


Most django projects I've seen don't use transactions and this app is designed for such projects.
>>>>>>> 613fcdf9bd6bca7d7bdee7468c077def5275d04e

## How does it work?

media_helper.cleanup connects pre_save and post_delete signals to special 
functions(these functions delete old files) for each model whose parent 
app is listed in INSTALLED_APPS above 'media_helper'.

media_helper.resizer assumes that when you upload an image, this image 
is intended to be an exact fit for the highest resolution version of your 
website/web-app, scales it down accordingly for different screen widths, 
and saves a copy in a folder corresponding to each resolution.  

For example, if you upload an image that is 800px wide with a maximum
screen-width defined to be 2560px, the 800px image will be saved in 
`MEDIA_ROOT` under the directory `2560/`, and a 400px wide version would
be saved in `1280/`.

The app then sets a session variable passed via a Jquery AJAX request,
so that when you insert an image with a template tag, the most
appropriately sized image will be delivered.

The directories created by `media_helper` mirrors the structure of each
`upload_to` path, so that in case a session variable is destroyed or
if the user


## Requirements

This app uses `Pillow` for image resizing.  If you've never used PIL or 
Pillow before, aside from the base package itself, you're going to need 
to make sure you have the appropriate development packages for each type
of image  you intend to encode.  

**IMPORTANT:  PIL/PIllow WILL 'successfully' install without the encoding
packages, but you won't be able to do much, so you need to install these 
packages BEFORE you try to install Pillow.**


For example, on a Debian-based system, the packages for JPEG's and PNG's 
are, respectively,

    libjpeg8-dev 
    libpng12-dev

And I believe on RPM systems, the only difference is "dev" becomes "devel."  
Whatever you're using, you will have to do something similar.  

And don't worry, Pillow pisses everyone off at some point.


## Installation
    
    pip install git+https://bitbucket.org/brmcllr/django_media_helper.git

Add media_helper to settings.py

    INSTALLED_APPS = (
        ...
        'media_helper', # should go after your apps
    )

<<<<<<< HEAD
`media_helper` should be placed after all your apps. (At least after those 
apps which need to remove files.)


The following urls are needed to set the session variable to track the 
resolution.Add the following to your root `urls.py`
=======
`*media_helper*` should be placed after all your apps. (At least after those apps which need to remove files.)


The following urls are needed to set the session variable to track the resolution. Add the following to 
your root `urls.py`
>>>>>>> 613fcdf9bd6bca7d7bdee7468c077def5275d04e

    urlpatterns = patterns('',
        ...
        url(r'^media-helper/', include('media_helper.urls')),
        ...
    )

We need the resizer.js file to set a session variable.  Of course you don't 
need this.  Feel free to set the variable anyway you wish. So let's collect 
the staticcfiles:

    ./manage.py collectstatic

<<<<<<< HEAD
If you're going to be using the template tag to deliver the new images, remember 
to restart yourserver after installing the package.

## Usage

The resizing and cleanup functions are done automatically.  Whenever an image 
is uploaded, changed, or deleted, the images will be resized or deleted for you.  
You don't need to do anything special.

But to integrate the resized images into your templates, you first need to add 
the JS source file.  Remember to add this after Jquery:

    {% static 'media-helper/resizer.js' %}

Now when you want to use a resized image, just use the `resolution` filter on an 
image in the `src` attribute in the `img` tag:

    <img src="{% resolution image %}}" />
=======
If you're going to be using the template tag to deliver the new images, remember to restart yourserver after 
installing the package.

## Usage

The resizing and cleanup functions are done automatically.  Whenever an image is uploaded, changed, or deleted, 
the images will be resized or deleted for you.  You don't need to do anything special.  But to integrate the 
resized images into your templates, you first need to add the JS source file.  Remember to add this after Jquery:

    {% static 'media-helper/resizer.js' %}

Now when you want to use a resized image, just use the `resolution` filter on an image in the `src` attribute in 
the `img` tag:
>>>>>>> 613fcdf9bd6bca7d7bdee7468c077def5275d04e

In this example `image` would be the context variable for an image field.

And that's it! Well, except for the other stuff...

## Configuration

Set `MEDIA_HELPER_AUTO_SIZES` to `False` if you want to explicitly specify which 
resolutions to resize for. Set it to `True` if you want a series of images to be 
generated between a certain range at even increments.

Default value: 
`MEDIA_HELPER_AUTO_SIZES = False`

If `MEDIA_HELPER_AUTO_SIZES` is `False`, define your screen widths in 
`MEDIA_HELPER_SIZES`.  It accepts a list of strings, integers, or floats.  I dont 
believe the order matters...i forgot if I implemented that though.  I probably did.  
just try it!  Be bold! Be swift! And damn the consequences!

Default value: 
`MEDIA_HELPER_AUTO_SIZES = [2560, 1920, 1600, 1440, 1366, 1280, 1024, 800]`

If `MEDIA_HELPER_AUTO_SIZES` is `True`, You need to set MEDIA_HELPER_MAX, 
MEDIA_HELPER_MIN, MEDIA_HELPER_STEP_SIZE.  MAX and MAX are both inclusive.  

Default values:
    MEDIA_HELPER_MAX = 2560
    MEDIA_HELPER_MIN = 800
    MEDIA_HELPER_STEP_SIZE = 320


## What it does **not** do (...yet?)

1. It does not scale up.  It only smaller images.

2. If the app was installed mid-project, legacy images will not be scaled

3. It does not scale images on the fly.
