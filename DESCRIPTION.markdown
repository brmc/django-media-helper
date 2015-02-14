# **django-media-helper** #

When dealing with content from unacquainted sources(e.g., clients or designers)
one often gets images with absurd dimensions and/or filesizes: A 3000px-wide
play-button, a 10MB logo, etc.  Media-helper attempts to mitigate this problem
by automating image-resizing, delivering the most appropriately sized image to
the browser.

It is also designed to be dropped into existing projects with minimal effort.
It's still in the alpha stage, but if you're careful it might make your life a
little bit easier while also speeding up your load times and reducing data
transfer.