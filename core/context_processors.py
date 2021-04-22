import re

from django.conf import settings



def metadata(request):
    """
    Add some generally useful metadata to the template context
    """
    return {'project_name': settings.PROJECT_NAME,
            'tagline': settings.TAGLINE,
            'homepage_url': settings.HOMEPAGE_URL}