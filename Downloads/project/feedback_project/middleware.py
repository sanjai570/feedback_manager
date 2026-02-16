# Middleware to handle dynamic Render.com domains
import logging
from django.core.exceptions import DisallowedHost
from django.http import HttpResponseBadRequest

logger = logging.getLogger(__name__)

class RenderAllowedHostsMiddleware:
    """
    Middleware to allow any *.onrender.com domain without adding them to ALLOWED_HOSTS.
    This is useful for Render deployments where the domain might change.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the HTTP_HOST header
        host = request.META.get('HTTP_HOST', '').split(':')[0]
        
        # Allow any onrender.com domain
        if host.endswith('.onrender.com') or host.endswith('onrender.com'):
            # Temporarily allow this host by adding it to ALLOWED_HOSTS
            from django.conf import settings
            if host not in settings.ALLOWED_HOSTS:
                settings.ALLOWED_HOSTS.append(host)
                logger.info(f"Dynamically added {host} to ALLOWED_HOSTS")
        
        # Allow localhost variants
        if host in ['localhost', '127.0.0.1', '0.0.0.0']:
            from django.conf import settings
            if host not in settings.ALLOWED_HOSTS:
                settings.ALLOWED_HOSTS.append(host)
        
        response = self.get_response(request)
        return response
