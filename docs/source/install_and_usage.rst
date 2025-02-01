.. _install:

Installation and usage
======================


Requirements
------------
Django Markdownify requires `Django <https://www.djangoproject.com/>`_ (obviously), as well as `Markdown <https://pypi.python.org/pypi/Markdown>`_ and
`Bleach <http://pythonhosted.org/bleach/index.html>`_ version 5 or higher. When installing Django Markdownify,
dependencies will be installed automatically.


Installation
------------
Install Django Markdownify with pip:

``pip install django-markdownify``

Or add ``django-markdownify`` to your requirements.txt and run ``pip install -r requirements.txt``

Finally add ``django_markdownify`` to your installed apps in ``settings.py``::

  INSTALLED_APPS = [
      ...
      'django_markdownify.apps.DjangoMarkdownifyConfig',
  ]

Usage
-----
Load the tag in your template:

``{% load markdownify %}``


Basic usage
^^^^^^^^^^^

Now you can change markdown to html as follows:

``{{ 'text'|django_markdownify }}``

Use Markdown in your template directly::

  {% load django_markdownify %}
  {{'Some *test* [link](#)'|django_markdownify }}


Or use the filter on a variable passed to the template via your views. For example::

  # views.py
  class MarkDown(TemplateView):
      template_name = 'index.html'

      def get_context_data(self, **kwargs):
          markdowntext = open(os.path.join(os.path.dirname(__file__), 'templates/test.md')).read()

          context = super().get_context_data(**kwargs)
          context['markdowntext'] = markdowntext

          return context

  # index.html
  {% load django_markdownify %}
  {{ markdowntext|django_markdownify }}

You probably want to add some extra allowed tags and attributes in the :doc:`settings`,
because the defaults are rather sparse.

It is possible to have different settings for different use cases, for example::

    # page1.html
    {{ markdowntext|django_markdownify }} <!-- uses the default settings -->

    # page2.html
    {{ markdowntext|django_markdownify:"restricted" }} <!-- uses the 'restricted' settings -->

See :doc:`settings` for a more detailed explanation.

Usage with tags
^^^^^^^^^^^^^^^

Alternatively you can put your text between the
``{% django_markdownify %}`` and ``{% endmdjango_markdownify %}`` tags::

  {% load django_markdownify %}

  {% django_markdownify %}
  Some *test* [link](#)
  {% enddjango_markdownify %}

This is useful if you are using Markdownify on another templatetag for example::

    {% load django_markdownify my_custom_template_tag %}

    {% django_markdownify %}
    {% my_custom_template_tag %}
    {% enddjango_markdownify %}

You can pass in the alternative settings as a parameter to the ``django_markdownify`` tag::

    {% load django_markdownify %}

    {% django_markdownify "restricted" %}
    Some *test* [link](#)
    {% enddjango_markdownify %}

Usage with filter
^^^^^^^^^^^^^^^^^

A third way is to use the ``filter`` tag::

    {% load django_markdownify %}

    {% filter django_markdownify %}
    [my link](https://{{domain}}.com)
    {% endfilter %}

This way, you can use dynamic content in your Markdown.

You can pass in the alternative settings as follows::

    {% filter django_markdownify:"restricted" %}


Settings
^^^^^^^^

To read about all the different configuration options, see :doc:`settings`.