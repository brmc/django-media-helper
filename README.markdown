# **django-media-helper** #

## Contents

* [Quick start](#quick-start)
* [Changelog (Recent changes only)](#changelog)
  * [v.0.2.1](#v021)
  * [v.0.1.4.bug-fix](#v014bug-fix)
  * [v.0.1.4  ](#v014)
  * [v.0.1.4.a](#v014a)
* [General Info](#general-info)
  * [File Cleanup](#file-cleanup)
  * [Image resizing](#image-resizing)
* [How does it work?](#how-does-it-work)
  * [File Cleanup](#file-cleanup-1)
  * [Image Resizing](#image-resizing-1)
  * [Something to consider](#something-to-consider)
* [Requirements](#requirements)
  * [Imaging](#imaging)
  * [Ajax](#ajax)
* [Installation](#installation)
* [Usage](#usage)
  * [Management Command: mediahelper](#management-command-mediahelper)
  * [option: --restore](#option---restore)
  * [option: --resize-all](#option---resize-all)
  * [option: --resize-originals](#option---resize-originals)
  * [option: --delete](#option---delete)
* [Configuration](#configuration)
  * [MEDIA_HELPER_AUTO](#media_helper_auto)
  * [MEDIA_HELPER_SIZES](#media_helper_sizes)
  * [MEDIA_HELPER_ROUND_TO](#media_helper_round_to)
  * [MEDIA_HELPER_MIN](#media_helper_min)
  * [MEDIA_HELPER_DEFAULT](#media_helper_default)
  * [MEDIA_HELPER_QUALITY](#media_helper_quality)
  * [MEDIA_HELPER_ALLOWED_ENCODINGS](#media_helper_allowed_encodings)
  * [MEDIA_HELPER_IMAGE_SELECTORS](#media_helper_image_selectors)
  * [MEDIA_HELPER_BACKGROUND_SELECTORS](#media_helper_background_selectors)
* [What it does not do (...yet?)](#what-it-does-not-do-yet)


## Quick start ##

i\. **Requirements**

1. Jquery
2. Pillow

1\. **Installation**

    pip install django-media-helper     

2\. **settings.py:**  
     
```
#!python

INSTALLED_APPS = (  
            ...  
            'media_helper', # should go after all your apps    
        )  
...

TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'media_helper.tools.context_processors.include_settings',
    )

```

2\. **urls.py:**

```
#!python

urlpatterns = patterns('',
        ...
        url(r'^media-helper/', include('media_helper.urls')),  
        ...
    )
```
3\. **Templates:**

    <script src="//code.jquery.com/jquery-1.11.0.min.js"></script>  
    {% include 'media_helper/ajax.html' %}

That should be it for default functionality  


## Changelog

### v.0.2.1

#### New features

* Added a context processor to access media_helper settings in templates.  
note:when accessing the settings, omit the `MEDIA_HELPER_` prefix.  That is  
simply to avoid namespace conflicts in the main django ecosystem.

* Added explicit include selectors for backgrounds and images.

#### Changes

* `resolution` view renamed to `media_helper`

* internal settings converted to uppercase.

### v.0.1.4.bug-fix

* fixed settings import error

* image size of 0 error fixed.  this was done earlier, but i forgot to mention
it

### v.0.1.4  

#### Changes

* tox and travis integration

* added python 3 compatibility

* moved to github 

### v.0.1.4.a


#### Changes

* settings module made less stupid.

* tests divded into separate files


#### General

* Flaked the shit out of everything



## General Info ##

This is a simple drop-in app that automates file deletion and image resizing.  
It should make your life a little bit easier while also speeding up your load   
times and reducing data transfer.  

It's basically broken into two parts.


### File Cleanup ###

First, this is a straight fork of `django-cleanup`, an app that deletes files   
from the server when the associated field or model is changed or deleted. It   
retains its complete functionality with virtually no modifications.  

From the django-cleanup docs:

    **Warning! If you use transactions you may lose you files if transaction   
    will rollback. If you are concerned about it you need other solution for   
    old file deletion in your project.**

    Most django projects I've seen don't use transactions and this app is   
    designed for such projects.

Full info here: https://github.com/un1t/django-cleanup


### Image resizing ###

Images are resized, stored, and delivered via AJAX while the rest of your page 
loads.


## How does it work? ##

### File Cleanup ###
`media_helper.tools.cleanup` connects pre_save and post_delete signals to special   
functions(these functions delete old files) for each model whose parent app    
is listed in INSTALLED_APPS above 'media_helper'.  


### Image Resizing ###
When you save an image, a couple things happen:  

1. The original image is copied to a new location and kept safe   
2. Several resized images will be initially generated (Info below)   
3. A default, low-res image will be also be created   

Images are also generated on the fly. 

When a user visits your domain, the low-res copy of each image will be used   
while the correctly sized images are being retrieved via AJAX calls.  If no   
image already exists, a new one will be re-sized. (this includes css   
background-images as well but not list-item-images).  If something goes wrong,  
the low-res image will remain in place.  

The size of the image will be determined by the html element's rendered size,  
and if the browser window is not maximized, it scales it up so image quality   
won't be lost in case the user **does** maximize the window. **This assumes  
you're using a responsive design with images whose sizes are not statically  
defined.  In the near future I will accomodate for for alternate scenarios**

**One person was under the impression that 3 requests were made per image  
(initial request, ajax, and the request for resized image), but that is not  
the case.  Well, it is true if there is only one image per page, but all  
ajax requests are bundled together, so the average number of requests  
approaches 2 as the number of images increases.**


### Something to consider ###

Resized images other than the default image are named and stored according to   
their size.  For example, if an image `foo.png` was resized to be 300px wide,   
it would be found under the following request path  

    /<MEDIA_URL>/media-helper/<upload_to>/foo.png/300.png  

It is warned that having purely numerical image names can negatively affect   
search results.  Nevertheless I have chosen to do so anyway because:  

1. the default image retains its original name, and from my understanding  
search engines index pages and images based on the results before the DOM  
is modified by javascript, so this should not affect indexing.  

2. any information found in the image name is retained in the full path.  

If I am mistaken, please let me know so I can rectify this as  
soon as possible.

So if you are uncertain and SEO is of utmost importance to you, you might   
reconsider using this app.


## Requirements ##

### Imaging ###
This app uses `Pillow` for image resizing.  If you've never used PIL or Pillow  
before, aside from the base library itself, you're going to need to make sure   
you have the appropriate development packages for each type of image you intend   
to encode.  

**IMPORTANT:  PIL/PIllow WILL 'successfully' install without the encoding  
packages, but you won't be able to do much, so you need to install these   
packages BEFORE you try to install Pillow.**  

Pay particular attention to this part:   
http://pillow.readthedocs.org/en/latest/installation.html#external-libraries  

And don't worry, Pillow pisses everyone off at some point.  


### Ajax ###

Unless you plan to write the client-side AJAX requests yourself, you're going  
to need jQuery.  It's pretty basic stuff, so any reasonably recent version   
should be fine.

`<script src="//code.jquery.com/jquery-1.11.0.min.js"></script>`  


## Installation ##

**1\.** Install media_helper:  
    
    pip install django-media-helper



**2\.** Add `media_helper` to settings.py

    INSTALLED_APPS = (
        ...
        'media_helper', # should go after your apps  
    )

`media_helper` should be placed after all your apps. (At least after those apps   
which need to remove files.)


**3.\** Add `media_helper.tools.context_processors.include_settings` to 
`TEMPLATE_CONTEXT_PROCESSORS` in settings.py

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'media_helper.tools.context_processors.include_settings',
    )

**3\.** In order to handle the ajax requests, add the following to your root `urls.py`  

    urlpatterns = patterns('',
        ...
        url(r'^media-helper/', include('media_helper.urls')),  
        ...
    )

  
  
**4\.** Now we also need some javascript, but the JS depends on some context variables,  
so include the following template somewhere *after* jquery, like so:  


    <script src="//code.jquery.com/jquery-1.11.0.min.js"></script>  
    ...
    {% include 'media_helper/ajax.html' %}  

(This is safe to use inside django-compressor `compress` tags)

And I write JS like a neanderthal, so feel free to write your own AJAX. I don't    
know if I'll get into the specifics in this version, but what I'm doing is     
pretty straight-forward and basic.  


## Usage ##

If you are content with the default settings(which just happen to be discussed   
next...spooky huh? Life is weird), for a new project, the rest is handled    
automatically.  You don't need to do anything else.   

However if you're adding this app to an existing project, or something seems to   
be broken,  here are some management commands that might be useful.  


### Management Command: `mediahelper` ###

**note: there aren't any tests written for these commands yet.  Use them at 
your own risk.  I've used them on three small sites in production without 
problem.** 

This command is used to retrofit the media_helper app into a project that  
already exists. With it you can resize all images found in the MEDIA_ROOT  
directory, resize/adjust the quality of the placeholder image, delete all  
resized images, and/or restore images to their original size, quality and  
location.  If all command options are used simultaneously, they will be  
processed in the following order:  
   --restore    
   --delete  
   --resize-originals  
   --resize-all  

And note that whenever --delete is passed, --restore will be forced so you  
don't risk losing your original images.  

**usage:**   
    python manage.py mediahelper <option>


### option: `--restore` ###

Restores the original images found in the media-helper sub directory to their  
native path and then deletes the backup.  All other images remain intact.  This  
means that the full-sized image will be delivered when the page is loaded.  


### option: `--resize-all`

Resizes all allowed images in MEDIA_ROOT.


### option: `--resize-originals`

Use this when you want to change the quality and/or size of the place holder   
images.  This just reinitializes everything, so for any changes to take affect  
you need to adjust the appropriate settings in your `settings.py`  


### option: `--delete`

Restores the original images and deletes the media-helper directory tree.  


## Configuration ##

Settings should be set in your `settings.py`

### `MEDIA_HELPER_AUTO`

A boolean that determines whether a series of images will be generated when a  
model is saved.  The auto-sizing feature expects your images to be consistently  
sized relative to one another and the final layout.  If your images are all   
willy-nilly, this probably won't do you much good.  More info in the next   
section.

**default value:**  `True`

### `MEDIA_HELPER_SIZES`

A list of scaling factors to be used to automatically scale images when they are   
saved.

**default values:**  
`[0.3, 0.3125, 0.4, 0.426953125, 0.45, 0.5, 0.53125, 0.546875, 0.5625, 0.6,  
0.625, 0.65625, 0.75, 0.8, 1.0]`

These values were chosen with a maximum screen width of 2560px in mind where    
each scaling factor corresponds to a common width.  For example:  
 
    1.0 ->  2560px
    .8  ->  2048px
    .75 ->  1920px
    ...
    .4  ->  1024px
    etc...

The assumption is that if a layout is designed for a 2560px width, each  
image is exactly cropped to fit the expected rendered dimensions of their html  
element with no stuffing or stretching going on.   

For example if you have a background-image, a logo, and a banner on a page where   
the background-image takes up the entire window, the banner is 80% of the screen   
width, and the logo is 10%, with the default settings `media-helper` expects you   
to upload images with the following widths:  

image          | width
--------------:|:------
background.jpg | 2560px
banner.jpg     | 2048px
logo.png       | 256px

So for the logo and background image, the auto-scaling feature would create the  
following sized images(widths are in px of course):  
    
scaling factor | 0.3 | 0.3125 | 0.4 | 0.426953125 | [...] | 0.75 | 0.8 | 1.0  
--------------:|-----|--------|-----|-------------|-------|------|-----|-----
background.jpg | 768 | 800    | 1024| 1093        | [...] | 1920 | 2048| 2560  
logo.png       | 77  | 80     | 103 | 110         | [...] | 193  | 205 | 256  

Two things to point out,

1. it always rounds up to the nearest pixel

2. this doesn't take into account any additional rounding preferences, making it 
a good time to go into that.


### `MEDIA_HELPER_ROUND_TO`

This is probably one of the most important features because it is intended to 
prevent a deluge of images being created, it is especially helpful for sites
with many images.

It is simply an integer representing the near # to round to.

**default value:** `10`

This value was chosen rather arbitrarily, but I figure it's large enough to 
account for slight variations in browsers.


### `MEDIA_HELPER_DEFAULT`

This is the scaling factor for the low-res default/placeholder.

**default value:** `.5`


### `MEDIA_HELPER_MIN`

The minimum allowed size for an image (in pixels).

**default  value:** `20`


### `MEDIA_HELPER_QUALITY`

The quality of the low-res image.

**default value:** `50`

default values for `MEDIA_HELPER_DEFAULT` and `MEDIA_HELPER_QUALITY` were also 
chosen without any particular reasoning other than "make smaller." No science
included.


### `MEDIA_HELPER_ALLOWED_ENCODINGS`

This tells media_helper which file extensions to recognize, but isn't checked 
intelligently.  It's simply a string comparison, but in case of errors, it 
should fail gracefully.

**default values:** `['jpg', 'jpeg', 'png']`


### `MEDIA_HELPER_IMAGE_SELECTORS`

A `string` of jQuery selectors for images to be resized (or ignored).

These can be any valid jQuery selector.  So you can make them as simple or  
complex as you wish. 

For example, both 'img' and '.container .img:not(nth-child(2))' would work.

This also combines the ALLOWED_ENCODINGS encodings, so the default settings  
produce:  

`$(img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"], )`

**default value:** `"img"`


### `MEDIA_HELPER_BACKGROUND_SELECTORS`

Like above, a string of jQuery selectors for elements with background-images  
to be resized.

These can be any valid jQuery selector.  So you can make them as simple or  
complex as you wish. 

For example, both 'div' and '.container .img:not(nth-child(2))' would work.

**default value:** `"div"`


## What it does **not** do (...yet?) ##

1. It does not scale up.  It only shrinks images.  

2. It doesn't resize images found under STATIC_URL

3. It doesn't handle javascript image zooming libraries very well, particularly  
if they source the same image or the display is set to none