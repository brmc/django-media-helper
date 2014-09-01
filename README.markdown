## django-media-helper

# Quick start

    pip install git+https://bitbucket.org/brmcllr/django_media_helper.git

settings.py:

    INSTALLED_APPS = (
            ...
            'media_helper', # should go after all your apps
        )
urls.py:

urlpatterns = patterns('',
        ...
        url(r'^media-helper/', include('media_helper.urls')),
        ...
    )

Ttemplates:

    <script src="//code.jquery.com/jquery-1.11.0.min.js"></script>
    {% include 'media-helper/ajax.html' %}

That should be it for default functionality

## General Info

This is a simple drop-in app that automates file deletion and image
resizing.  It should make your life a little bit easier while also 
speeding up your load times and reducing data transfer.

It's basically broken into two parts.

`media_helper.cleanup:`

First, this is a straight fork of `django-cleanup`, an app that deletes files 
from the server when the associated field or model is changed or deleted. 
It retains its complete functionality with virtually no modifications.

`media_helper.resizer`

Images are resized images for you and delivered via AJAX while the rest of 
your page loads.

From the django-cleanup docs:

    **Warning! If you use transactions you may lose you files if transaction 
    will rollback. If you are concerned about it you need other solution for 
    old file deletion in your project.**

    Most django projects I've seen don't use transactions and this app is 
    designed for such projects.


## How does it work?

# Cleanup
`media_helper.cleanup` connects pre_save and post_delete signals to special 
functions(these functions delete old files) for each model whose parent 
app is listed in INSTALLED_APPS above 'media_helper'.


# Resizer
When you save an image, a couple things happen:

1. The original image is copied to a new location and kept safe
2. Several resized images will be initially generated (Info below)
3. A default, low-res image will be also be created

When a user visits your domain, the low-res copy of each image will be used 
while the correctly sized images are being delivered via AJAX calls.  If no 
image already exists, a new one will be re-sized. (this includes css 
background-images as well but not list-item-images).  If something goes 
wrong,the low-res image will remain in place.

# Something to consider

Resized images other than the default image are named and stored according 
to their size.  For example, if an image `foo.png` was resized to be 300px 
wide, it would be found under the following request path

    /<MEDIA_URL/media-helper/<upload_to>/foo.png/300.png

It is warned that having purely numerical image names can negatively affect 
search results.  Nevertheless I have chosen to do so because:

1. the default image retains its original name, and from my understanding
search engines index pages and images based on the results before the DOM
is modified by javascript, so this should not affect indexing.

2. any information found in the image name is retained in the full path.

If my understanding is mistaken, please let me know so I can rectify this
as soon as possible.

So if you are uncertain and SEO is of utmost importance to you, you might 
reconsider using this app.


## Requirements

# Imaging
This app uses `Pillow` for image resizing.  If you've never used PIL or 
Pillow before, aside from the base library itself, you're going to need 
to make sure you have the appropriate development packages for each type
of image you intend to encode.  

**IMPORTANT:  PIL/PIllow WILL 'successfully' install without the encoding
packages, but you won't be able to do much, so you need to install these 
packages BEFORE you try to install Pillow.**

Pay particular attention to this part: 
http://pillow.readthedocs.org/en/latest/installation.html#external-libraries

And don't worry, Pillow pisses everyone off at some point.

# Ajax

Unless you plan to write the client-side AJAX requests yourself, you're going
to need jQuery.  It's pretty basic stuff, so any reasonably recent version 
should be fine.

`<script src="//code.jquery.com/jquery-1.11.0.min.js"></script>`


## Installation
    
    pip install git+https://bitbucket.org/brmcllr/django_media_helper.git

Add `media_helper` to settings.py

    INSTALLED_APPS = (
        ...
        'media_helper', # should go after your apps
    )

`media_helper` should be placed after all your apps. (At least after those 
apps which need to remove files.)

In order to handle the ajax requests, add the following to your root `urls.py`

    urlpatterns = patterns('',
        ...
        url(r'^media-helper/', include('media_helper.urls')),
        ...
    )

Now we also need some javascript, but the JS depends on some context variables,
so include the following template somewhere *after* jquery, like so:


    <script src="//code.jquery.com/jquery-1.11.0.min.js"></script>
    ...
    {% include 'media-helper/ajax.html' %}

And I write JS like a neanderthal, so feel free to write your own AJAX.
I don't know if I'll get into the specifics in this version, but what I'm doing 
is pretty straight-forward and basic.


## Usage

The rest is handled automatically.  Unless you want to configure things

## Configuration

** There are several deprecated settings below, so be 

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
MEDIA_HELPER_MIN, MEDIA_HELPER_STEP_SIZE.  MAX andMAX are both inclusive.  

Default values:
    MEDIA_HELPER_MAX = 2560
    MEDIA_HELPER_MIN = 800
    MEDIA_HELPER_STEP_SIZE = 320


## What it does **not** do (...yet?)

1. It does not scale up.  It only smaller images.

2. If the app was installed mid-project, legacy images will not be scaled

3. It does not scale images on the fly.