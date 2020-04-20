
import mechanize

from ApiCalls import ApiClient

base_url = "http://localhost:8001"
REDIRECT_URI = 'http://0.0.0.0:8001/'
AUTHORIZE_URL = "http://0.0.0.0:8001/oauth/authorize"
ACCESS_TOKEN_URL = "http://0.0.0.0:8001/oauth/token"

def lifecycle(email, pw, client_id, client_secret):
    global base_url

    cli = ApiClient(client_id, client_secret, REDIRECT_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL,
                    "trashuserzths@protonmail.com", "qwerty1234", base_url)

    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent', 'Firefox')]
    browser.open(base_url)
    browser.select_form(nr = 0)
    browser.form["email"] = email
    browser.form["password"] = pw
    sub = browser.submit()
    print(sub.read())
    print(cli.get_budgets())

lifecycle("trashuserzths@protonmail.com", "qwerty1234", "3", "6Eb11vg04jHsCcYeOCCtREF6LX7TRRkYgxtA7vlG")

