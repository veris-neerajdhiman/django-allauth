from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import VerisProvider

urlpatterns = default_urlpatterns(VerisProvider)
