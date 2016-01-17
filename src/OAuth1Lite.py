from urllib import quote
from urlparse import parse_qs, urlparse, urlunparse
from oauthlib.oauth1.rfc5849.signature import normalize_base_string_uri, normalize_parameters, \
                                              construct_base_string, sign_hmac_sha1
from oauthlib.oauth1.rfc5849.parameters import prepare_headers
from oauthlib.common import generate_nonce, generate_timestamp
from requests.auth import AuthBase


class OAuth1Lite(AuthBase):
    """
    Yahoo requires special handling, since they do not support OAuth2, but have added support for
    reusable tokens by amending RFC5849. This requires the additional parameter, oauth_session_handle,
    which is not apart of the official OAuth1 specification (RFC5849). Yahoo documents this here
    http://oauth.googlecode.com/svn/spec/ext/session/1.0/drafts/1/spec.html#anchor4.
    And since, AFAIK, rauth and requests-oauthlib do not allow easy addition
    of parameters to the authorization header, we setup a class to allow for an arbitrary
    number of authorization parameters.
    """
    def __init__(self, client_key, client_secret, oauth_token='', oauth_token_secret='', callback=None):
        self.client_key = unicode(client_key)
        self.client_secret = unicode(client_secret)
        self.oauth_token = unicode(oauth_token)
        self.oauth_token_secret = unicode(oauth_token_secret)
        self.callback = unicode(callback)
        self.params = [
            (u'oauth_consumer_key', self.client_key),
            (u'oauth_version',  u'1.0'),
            ]
        if callback:
            self.add_param(u'oauth_callback', self.callback)
        if oauth_token:
            self.add_param(u'oauth_token', self.oauth_token)
            self.add_param(u'oauth_token_secret', self.oauth_token_secret)

    def __call__(self, request):
        """
        Uses the prepared request passed in by the requests library, and adds the necessary authorization
        header and signature for OAuth1
        See example here: http://docs.python-requests.org/en/latest/user/advanced/#custom-authentication
        """
        parse_url = urlparse(request.url)
        self.add_params(parse_qs(parse_url.query))
        request.url = urlunparse(parse_url)

        self.sign(request.url, method=request.method)
        request.headers.update(self.create_authorization_header())
        return request

    def add_param(self, field, value):
        self.params.append((unicode(field), unicode(value)))

    def add_params(self, params={}):
        for (k, v) in params.items():
            if type(v) == list:
                for i in v:
                    self.add_param(k, i)
            else:
                self.add_param(k, v)

    def find_param_idx(self, field):
        for (i, (k, v)) in enumerate(self.params):
            if k == field:
                return i
        return None

    def update_param(self, params={}):
        """
        Updates value of parameter if found, otherwise adds it
        :param params: parameters as dictionary
        :return:
        """
        for (k, v) in params.items():
            update_idx = self.find_param_idx(k)
            if update_idx:
                self.params[update_idx] = v
            else:
                self.add_param(k, v)

    def sign(self, url, method=u'POST', signature_method=u'HMAC-SHA1'):
        """
        Use this method to create a signature over the authorization header, and the url query parameters
        :param url: request url
        :param method: request method (i.e. POST, GET)
        :param signature_method: method of signature. Only supports (HMAC-SHA1, PLAINTEXT)
        Note: that HMAC-SHA1 is required by Yahoo API queries since they are sent insecurely
        """
        # could change this to support additional methods
        # for now only support HMAC-SHA1 and PLAINTEXT (Yahoo only supports these)
        self.add_param(u'oauth_signature_method', signature_method)
        self.add_param(u'oauth_nonce', generate_nonce())
        self.add_param(u'oauth_timestamp', generate_timestamp())
        if signature_method == u'HMAC-SHA1':
            base_string = construct_base_string(unicode(method),
                                                normalize_base_string_uri(unicode(url)),
                                                normalize_parameters(self.params))
            signature = sign_hmac_sha1(base_string, self.client_secret, self.oauth_token_secret)
        else:
            signature = quote(self.client_secret + u'&' + self.oauth_token_secret)
        self.add_param(u'oauth_signature', signature)

    def create_authorization_header(self):
        return prepare_headers(self.params)

    def sign_and_create_authorization_header(self, url, token_secret, method=u'POST', signature_method=u'HMAC-SHA1'):
        self.sign(url, token_secret, method, signature_method)
        return self.create_authorization_header()