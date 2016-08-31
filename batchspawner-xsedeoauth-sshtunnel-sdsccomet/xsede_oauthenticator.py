from oauthenticator.cilogon import CILogonOAuthenticator
from tornado.httpclient import HTTPRequest
from urllib.parse import parse_qs
from jupyterhub.utils import url_path_join as ujoin
from tornado.httputil import url_concat
from tornado import gen

try:
    from OpenSSL.crypto import load_certificate, FILETYPE_PEM
except ImportError:
    raise ImportError("CILogon OAuth requires PyOpenSSL")

class XSEDEOAuthenticator(CILogonOAuthenticator):
    """Use XSEDE oauth service

    it allows to authenticate users and get a certificate so we can
    login with gsissh to Comet and launch a job on the user's behalf,
    resources will be charged on the allocation of the user.
    """
    authorization_url = "https://oa4mp.xsede.org/oauth/authorize"
    cilogon_skin = "xsede"
    oauth_url = "https://oa4mp.xsede.org/oauth"
    login_service = "XSEDE"

    @gen.coroutine
    def username_from_token(self, token):
        """Turn a user token into a username

        Username is stored differently than CILogon"""
        uri = url_concat(ujoin(self.oauth_url, 'getcert'), {
            'oauth_token': token,
        })
        uri, _, _ = self.oauth_client.sign(uri)
        resp = yield self.client.fetch(uri)
        # FIXME: handle failure
        reply = resp.body.decode('utf8', 'replace')
        username_string, cert_txt = reply.split('\n', 1)
        username_string_splitted = username_string.split('=', 1)

        if len(username_string_splitted) != 2:
            raise ValueError("Failed to get username from: %s", username_string)

        username = username_string_splitted[1]
        return username, cert_txt

    @gen.coroutine
    def get_oauth_token(self):
        """Get the temporary OAuth token

        Compared to the CILogonOAuthenticator we also set the lifetime and do
        more logging, everything else is the same"""
        uri = url_concat(ujoin(self.oauth_url, "initiate"), {
            'oauth_callback': self.oauth_callback_url,
            'certreq': self.certreq,
            'certlifetime': 3600*24*10
        })
        self.log.info("OAuth initiate URI: %s", str(uri))
        uri, _, _ = self.oauth_client.sign(uri)
        self.log.info("OAuth initiate URI signed: %s", str(uri))
        req = HTTPRequest(uri)
        # FIXME: handle failure (CILogon replies with 200 on failure)
        resp = yield self.client.fetch(req)
        reply = resp.body.decode('utf8', 'replace')
        credentials = parse_qs(reply)
        self.log.info("Parsed credentials: %s", str(credentials))
        return credentials['oauth_token'][0]
