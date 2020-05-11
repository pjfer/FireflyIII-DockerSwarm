import json
import time

import mechanize
import requests
from random import randint


class ApiClient:
    """
        Initialize the client and create an account.
    """
    def __init__(self, base_url, redirect_uri, authorize_url,
                 access_token_url, email, pw, client_id=None, client_secret=None):

        # Start Browser Crawler
        self.browser_cookies = {}
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent', 'Firefox')]
        self.base_url = base_url

        # Set API and OAuth2 variables
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.api_cookies = {}
        self.api_headers = {}
        self.user_id = 0

        # Access Credentials
        self.email = email
        self.pw = pw

        # The account doesn't exist.
        if client_id is None:
            self.create_user()
            self.get_access_token(True)
        else:
            self.get_access_token(False)

    '''
        Creates the user using the email and pw given in the constructor.
    '''
    def create_user(self):
        # Opens the browser.
        self.br.open(self.base_url)

        # Selects create account.
        for link in self.br.links():
            if link.text == "Register a new account":
                self.br.follow_link(link)
                break

        # Fills the credentials and submits the creation.
        self.br.select_form(nr=0)
        self.br.form["email"] = self.email
        self.br.form["password"] = self.pw
        self.br.form["password_confirmation"] = self.pw
        self.br.submit()

        # Stores the cookies needed to browse the application using get requests.
        for c in self.br._ua_handlers['_cookies'].cookiejar:
            self.browser_cookies[c.name] = c.value

        # Loads a js file that contains the token needed to request a new OAuth2 client.
        response = requests.get(self.base_url + "/v1/jscript/variables?ext=.js&v=5.2.2", cookies=self.browser_cookies)
        token = ""

        # Obtains the token.
        for line in response.content.decode("utf-8").split("\n"):
            if line.split("=")[0] == "var token ":
                token = line.split("=")[1].split("'")[1]

        # Generates the request for a new OAuth2 client.
        data = {
            "name": "api_usage",
            "redirect": self.redirect_uri
        }
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        response = requests.post(
            url=self.base_url + "/oauth/clients?_token=" + token,
            data=json.dumps(data),
            headers=headers,
            cookies=self.browser_cookies
        ).json()

        # Stores the OAuth2 Client information.
        self.client_id = response["id"]
        self.client_secret = response["secret"]
        self.user_id = response["user_id"]

    '''
        Obtains the token to execute API calls using the client_id and secret.
    '''
    def get_access_token(self, first):
        # Starts a local browser to access the authorize url.
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]
        br.open('{}?response_type=code&client_id={}&redirect_uri={}'.format(self.authorize_url,
                                                                            self.client_id, self.redirect_uri))
        # Realizes the login using the email and pw of the user.
        br.select_form(nr=0)
        br.form["email"] = self.email
        br.form["password"] = self.pw
        br.submit()

        if first:
            # Selects the authorize for the first time run.
            br.select_form(nr=0)
            br.submit()

        # Obtains the code returned in the redirected url.
        code = str(br.geturl()).split("?")[1].split("=")[1]

        # Using the code in the redirected url, obtain a token to use the API.
        token = requests.post(
            self.access_token_url,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri
            },
        ).json()["access_token"]

        # Generates the headers and cookies used in the API requests.
        self.api_cookies = {"XSRF-TOKEN": token, "firefly_session": token}
        self.api_headers = {"accept": "application/json",
                            "Authorization": "Bearer " + token,
                            "Content-Type": "application/json"}

    '''
        Executes the login with the given email and pw.
    '''
    def login(self):
        # Creates a browser in the starting url.
        self.br.open(self.base_url)

        # Executes the login
        self.br.select_form(nr=0)
        self.br.form["email"] = self.email
        self.br.form["password"] = self.pw
        self.br.submit()

        # Stores the cookies needed to browse the application using get requests.
        for c in self.br._ua_handlers['_cookies'].cookiejar:
            self.browser_cookies[c.name] = c.value

    '''
        Load simulator (requests the resources for the dashboard that the simple crawler doesn't ask.)
    '''
    def load_dashboard_resources(self):
        requests.get(self.base_url + "/chart/account/frontpage", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/bill/frontpage", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/budget/frontpage", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/category/frontpage", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/account/expense", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/account/revenue", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/box/balance", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/box/bills", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/box/available", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/box/net-worth", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/frontpage/piggy-banks", cookies=self.browser_cookies).json()

    '''
        Clicks in the Asset accounts link.
    '''
    def enter_assets(self):
        for link in self.br.links():
            if link.text == "Asset accounts":
                self.br.follow_link(link)
                break

    '''
       Clicks in the Create an asset account link.
       And fills the form to create the account.
    '''
    def create_asset_account(self):
        for link in self.br.links():
            if link.text == "Create an asset account":
                self.br.follow_link(link)
                break

        # Selects the form for the account and fills it.
        self.br.select_form(nr=1)
        self.br.form["name"] = "Conta Corrente: " + self.email
        self.br.form["opening_balance"] = str(randint(500, 1000))
        self.br.form["opening_balance_date"] = "2020-03-01"
        self.br.submit()

    '''
        Clicks in the Expense accounts link.
    '''
    def enter_expenses(self):
        for link in self.br.links():
            if link.text == "Expense accounts":
                self.br.follow_link(link)
                break

    '''
        Clicks in the Create an expense account link.
        And creates an expense account.
    '''
    def create_expense_account(self):
        for link in self.br.links():
            if link.text == "Create an expense account":
                self.br.follow_link(link)
                break

        # Selects the form for the account and fills it.
        self.br.select_form(nr=1)
        self.br.form["name"] = "Supermercado: " + self.email
        self.br.submit()

    '''
        Clicks in the Revenue accounts link.
    '''
    def enter_revenue(self):
        for link in self.br.links():
            if link.text == "Revenue accounts":
                self.br.follow_link(link)
                break

    '''
        Clicks in the Create a revenue account link.
        And creates an expense account.
    '''
    def create_revenue_account(self):
        for link in self.br.links():
            if link.text == "Create a revenue account":
                self.br.follow_link(link)
                break

        # Selects the form for the account and fills it.
        self.br.select_form(nr=1)
        self.br.form["name"] = "Empregador: " + self.email
        self.br.submit()

    '''
        Clicks in the Liabilities link.
    '''
    def enter_liabilities(self):
        for link in self.br.links():
            if link.text == "Liabilities":
                self.br.follow_link(link)
                break

    '''
        Clicks in the Create a liability link.
        And creates an expense account.
    '''
    def create_liability(self):
        for link in self.br.links():
            if link.text == "Create a liability":
                self.br.follow_link(link)
                break

        # Selects the form for the account and fills it.
        self.br.select_form(nr=1)
        self.br.form["name"] = "Empréstimo casa: " + self.email
        self.br.form["opening_balance"] = str(randint(50000, 100000))
        self.br.form["opening_balance_date"] = "2010-03-01"
        self.br.form["interest"] = "6"
        self.br.submit()

    '''
        Clicks in the Categories link.
    '''
    def enter_categories(self):
        for link in self.br.links():
            if link.text == "Categories":
                self.br.follow_link(link)
                break

    '''
        Clicks in the Create a category link.
        And creates multiple categories.
    '''
    def create_categories(self):
        categories = ["Roupa: ", "Comida: ", "Carro: ", "Mobilia: ", "Eletrodomésticos: "]

        # For each category.
        for c in categories:

            # Enter the create category link.
            for link in self.br.links():
                if c == "Roupa":
                    if link.text == "Create a category":
                        self.br.follow_link(link)
                else:
                    if link.text == "New category":
                        self.br.follow_link(link)

            # Selects the form for the account and fills it.
            self.br.select_form(nr=1)
            self.br.form["name"] = c + self.email
            self.br.submit()
            time.sleep(randint(1, 5))
            print("Category created")

    '''
        Clicks in the Expenses link.
    '''
    def enter_transactions_expenses(self):
        for link in self.br.links():
            if link.text == "Expenses":
                self.br.follow_link(link)
                break

    '''
        Load simulator (requests the resources for the expenses transactions that the simple crawler doesn't ask.)
    '''
    def load_transactions_expenses(self):
        requests.get(self.base_url + "/chart/transactions/categories/withdrawal/2020-03-01/2020-03-31",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/transactions/budgets/2020-03-01/2020-03-31",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/transactions/destinationAccounts/withdrawal/2020-03-01/2020-03-31",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/currencies", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/budgets", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/piggy-banks", cookies=self.browser_cookies).json()
        requests.get(url=self.base_url + "/api/v1/preferences", headers=self.api_headers).json()

    '''
        Does multiple api requests to generate multiple transactions.
    '''
    def create_transactions_expenses(self):
        # The expenses transactions are applied to a random category
        categories = ["Roupa: ", "Comida: ", "Carro: ", "Mobilia: ", "Eletrodomésticos: "]

        # Generates 100 transactions
        for i in range(0, 100):
            c = randint(0, 4)  # Index of the category.

            n = randint(1, 31)  # Day of the transaction.
            if n >= 10:
                date = "2020-03-" + str(n)
            else:
                date = "2020-03-0" + str(n)

            # Generates the transaction.
            transaction = {"type": "withdrawal",
                           "date": date,
                           "amount": str(randint(5, 15)),
                           "description": "Expenses",
                           "source_name": "Conta Corrente: " + self.email,
                           "destination_name": "Supermercado: " + self.email,
                           "category_name": categories[c] + self.email
                           }
            data = {
                "user": self.user_id,
                "transactions": [transaction]
            }

            # Executes the API request.
            requests.post(
                url=self.base_url + "/api/v1/transactions",
                data=json.dumps(data),
                headers=self.api_headers
            ).json()
            time.sleep(randint(1, 5))
            print("Expense transaction created")
    '''
        Clicks in the Revenue / income link.
    '''
    def enter_transactions_revenue(self):
        for link in self.br.links():
            if link.text == "Revenue / income":
                self.br.follow_link(link)
                break

    '''
        Load simulator (requests the resources for the revenue transactions that the simple crawler doesn't ask.)
    '''
    def load_transactions_revenue(self):
        requests.get(self.base_url + "/chart/transactions/categories/deposit/2020-03-01/2020-03-30",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/transactions/destinationAccounts/deposit/2020-03-01/2020-03-30",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/transactions/sourceAccounts/deposit/2020-03-01/2020-03-30",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/currencies", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/budgets", cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/json/piggy-banks", cookies=self.browser_cookies).json()
        requests.get(url=self.base_url + "/api/v1/preferences/transaction_journal_optional_fields",
                     headers=self.api_headers).json()

    '''
        Does one api requests to generate the salary transaction.
    '''
    def create_transactions_revenue(self):

        transaction = {"user": self.user_id,
                       "type": "deposit",
                       "date": "2020-03-01",
                       "amount": "1000",
                       "description": "Salary",
                       "source_name": "Empregador: " + self.email,
                       "destination_name": "Conta Corrente: " + self.email,
                       }
        data = {
            "user": self.user_id,
            "transactions": [transaction]
        }

        requests.post(
            url=self.base_url + "/api/v1/transactions",
            data=json.dumps(data),
            headers=self.api_headers
        ).json()

    '''
        Clicks in the Reports link.
    '''
    def enter_reports(self):
        for link in self.br.links():
            if link.text == "Reports":
                self.br.follow_link(link)
                break

    '''
        Load simulator (requests the resources for the Reports that the simple crawler doesn't ask.)
    '''
    def load_reports(self):
        requests.get(self.base_url + "/reports/options/audit", cookies=self.browser_cookies).json()

    '''
        Clicks in the Last month, all accounts link.
    '''
    def enter_month_balance(self):
        for link in self.br.links():
            if link.text == "Last month, all accounts":
                self.br.follow_link(link)
                break

        return self.br.geturl().split("/")[5]

    '''
        Load simulator (requests the resources for the Last Month report page that the simple crawler doesn't ask.)
    '''
    def load_month_balance(self, id):
        requests.get(self.base_url + "/report-data/account/general/" + id + "/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/income/" + id + "/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/expenses/" + id + "/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/operations/" + id + "/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/bill/overview/" + id + "/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/chart/account/report/" + id + "/20200301/20200331",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/report-data/budget/general/" + id + "/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/balance/general/" + id + "/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/category/operations/" + id + "/20200301/20200331",
                     cookies=self.browser_cookies)

    '''
        Clicks in the Current year, all accounts link.
    '''
    def enter_year_balance(self):
        for link in self.br.links():
            if link.text == "Current year, all accounts":
                self.br.follow_link(link)
                break

        return self.br.geturl().split("/")[5]

    '''
        Load simulator (requests the resources for the Current year report page that the simple crawler doesn't ask.)
    '''
    def load_year_balance(self, id):
        requests.get(self.base_url + "/report-data/account/general/" + id + "/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/income/" + id + "/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/expenses/" + id + "/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/operations/" + id + "/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/reports/default/" + id + "/currentYearStart/currentYearEnd",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/chart/report/net-worth/" + id + "/20200101/20201231",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/report/operations/" + id + "/20200101/20201231",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/report-data/budget/period/" + id + "/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/category/expenses/" + id + "/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/category/income/" + id + "/20200101/20201231",
                     cookies=self.browser_cookies)
    '''
        Returns the credentials used to access the api.
    '''
    def get_api_credentias(self):
        return self.client_id, self.client_secret
