from django import template

register = template.Library()

@register.simple_tag(takes_context = True)
def resolution(context, image):
    import os
    resolution = context['request'].session['resolution']
    path = context['MEDIA_URL']
    return os.path.join(path, resolution, image.name)