import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from .provider import VerisProvider


class VerisOAuth2Adapter(OAuth2Adapter):
    provider_id = VerisProvider.id
    access_token_url = 'http://local.veris.in:8001/o/token/'
    authorize_url = 'http://local.veris.in:8001/o/authorize/'
    profile_url = 'http://local.veris.in:8001/me/'

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            params={'access_token': token.token,
                                    'alt': 'json'})
        resp.raise_for_status()
        extra_data = resp.json()
        login = self.get_provider() \
            .sociallogin_from_response(request,
                                       extra_data)
        return login


oauth2_login = OAuth2LoginView.adapter_view(VerisOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(VerisOAuth2Adapter)
