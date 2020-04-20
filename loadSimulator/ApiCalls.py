
import requests
import mechanize


class ApiClient:

    def __init__(self, client_id, client_secret, redirect_uri, authorize_url, access_token_url, email, pw, base_url):

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.email = email
        self.pw = pw
        self.base_url = base_url

        self.get_access_token()

    def get_access_token(self):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]
        response = br.open(
            '{}?response_type=code&client_id={}&redirect_uri={}'.format(self.authorize_url,
                                                                        self.client_id, self.redirect_uri))
        br.select_form(nr=0)
        br.form["email"] = self.email
        br.form["password"] = self.pw
        br.submit()

        code = str(br.geturl()).split("?")[1].split("=")[1]

        response = requests.post(
            self.access_token_url,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri
            },
        )
        self.token = response.json()["access_token"]
        self.cookies = {"XSRF-TOKEN": self.token, "firefly_session": self.token}
        self.headers = {"authorization": "Bearer "+self.token}


    def get_budgets(self):
        return requests.get(self.base_url+"/api/v1/available_budgets", cookies=self.cookies, headers=self.headers).json()
