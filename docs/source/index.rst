.. DjangoMarkdownify documentation master file, created by
   sphinx-quickstart on Fri Jan 19 12:58:03 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



.. toctree::
   :maxdepth: 1
   :caption: Table of contents
   :name: maintoc

   Introduction <self>
   Installation and usage <install_and_usage>
   Settings <settings>
   Tests <tests>

Django Markdownify - A Django Markdown filter
=============================================
**Django Markdownify is a template filter to convert Markdown to HTML in Django.
Markdown is converted to HTML and sanitized.**

Example::

  {% load django_markdownify %}
  {{'Some *test* [link](#)'|django_markdownify }}

Is transformed to::

  <p>
    Some <em>test</em> <a href="#">link</a>
  </p>

The filter is a wrapper around `Markdown <https://pypi.python.org/pypi/Markdown>`_ and
`Bleach <http://pythonhosted.org/bleach/index.html>`_ and as such supports their settings. It is possible to define multiple settings for multiple usecases.

For example::

   # settings.py

   MARKDOWNIFY = {
      "default": {
         "WHITELIST_TAGS": ["a", "p", "h1", ]
      },

      "alternative": {
         "WHITELIST_TAGS": ["a", "p", ],
         "MARKDOWN_EXTENSIONS": ["markdown.extensions.fenced_code", ]
      }
   }

And in your templates::

   <!-- page1.html -->
   {{ mytext|django_markdownify }} <!-- Uses your default settings -->

   <!-- page2.html -->
   {{ mytext|django_markdownify:"alternative" }} <!-- Uses your alternative settings -->

The code can be found on `Github <https://github.com/erwinmatijsen/django-markdownify>`_.
