from allauth.account.models import EmailAddress
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import (ProviderAccount,
                                                  AuthAction)
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.app_settings import QUERY_EMAIL


class Scope(object):
    # EMAIL = 'email'
    PROFILE = 'profile'


class VerisAccount(ProviderAccount):
    # def get_profile_url(self):
    #     return self.account.extra_data.get('link')

    # def get_avatar_url(self):
    #     return self.account.extra_data.get('picture')

    def to_str(self):
        dflt = super(VerisAccount, self).to_str()
        return self.account.extra_data.get('first_name', dflt) + ' ' + self.account.extra_data.get('last_name', dflt)


class VerisProvider(OAuth2Provider):
    id = 'veris'
    name = 'Veris'
    account_class = VerisAccount

    def get_default_scope(self):
        scope = [Scope.PROFILE]
        # if QUERY_EMAIL:
        #     scope.append(Scope.EMAIL)
        return scope

    def get_auth_params(self, request, action):
        ret = super(VerisProvider, self).get_auth_params(request,
                                                          action)
        if action == AuthAction.REAUTHENTICATE:
            ret['prompt'] = 'select_account'
        return ret

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(email=data.get('email'),
                    last_name=data.get('last_name'),
                    first_name=data.get('first_name'))

    def extract_email_addresses(self, data):
        ret = []
        email = data.get('email')
        # if email and data.get('verified_email'):
        ret.append(EmailAddress(email=email,
                   verified=True,
                   primary=True))
        return ret


providers.registry.register(VerisProvider)
