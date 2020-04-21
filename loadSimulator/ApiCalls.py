import json

import mechanize
import requests
from random import randint

class ApiClient:

    def __init__(self, email, pw, base_url, client_id, client_secret, redirect_uri, authorize_url, access_token_url):
        self.browser_cookies = {}
        self.email = email
        self.pw = pw
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent', 'Firefox')]
        self.base_url = base_url
        self.api_headers = {}

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.api_cookies = {}
        self.api_headers = {}

        self.get_access_token()

    def get_access_token(self):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]
        br.open('{}?response_type=code&client_id={}&redirect_uri={}'.format(self.authorize_url,
                                                                            self.client_id, self.redirect_uri))

        br.select_form(nr=0)
        br.form["email"] = self.email
        br.form["password"] = self.pw
        br.submit()

        code = str(br.geturl()).split("?")[1].split("=")[1]

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

        self.api_cookies = {"XSRF-TOKEN": token, "firefly_session": token}
        self.api_headers = {"accept": "application/json",
                            "Authorization": "Bearer "+token,
                            "Content-Type": "application/json"}

    def login(self):
        self.br.open(self.base_url)
        self.br.select_form(nr=0)
        self.br.form["email"] = self.email
        self.br.form["password"] = self.pw
        self.br.submit()
        for c in self.br._ua_handlers['_cookies'].cookiejar:
            self.browser_cookies[c.name] = c.value

    def get_budgets(self):
        return requests.get(self.base_url + "/api/v1/available_budgets", cookies=self.api_cookies,
                            headers=self.api_headers).json()

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

    def enter_assets(self):
        for link in self.br.links():
            if link.text == "Asset accounts":
                self.br.follow_link(link)
                break

    def create_asset_account(self):
        for link in self.br.links():
            if link.text == "Create an asset account":
                self.br.follow_link(link)
                break

        self.br.select_form(nr=1)
        self.br.form["name"] = "Conta Corrente: "+self.email
        self.br.form["opening_balance"] = str(randint(500, 1000))
        self.br.form["opening_balance_date"] = "2020-03-01"
        self.br.submit()

    def enter_expenses(self):
        for link in self.br.links():
            if link.text == "Expense accounts":
                self.br.follow_link(link)
                break

    def create_expense_account(self):
        for link in self.br.links():
            if link.text == "Create an expense account":
                self.br.follow_link(link)
                break

        self.br.select_form(nr=1)
        self.br.form["name"] = "Supermercado: "+self.email
        self.br.submit()

    def enter_revenue(self):
        for link in self.br.links():
            if link.text == "Revenue accounts":
                self.br.follow_link(link)
                break

    def create_revenue_account(self):
        for link in self.br.links():
            if link.text == "Create a revenue account":
                self.br.follow_link(link)
                break

        self.br.select_form(nr=1)
        self.br.form["name"] = "Empregador: "+self.email
        self.br.submit()

    def enter_liabilities(self):
        for link in self.br.links():
            if link.text == "Liabilities":
                self.br.follow_link(link)
                break

    def create_liability(self):
        for link in self.br.links():
            if link.text == "Create a liability":
                self.br.follow_link(link)
                break

        self.br.select_form(nr=1)
        self.br.form["name"] = "Empréstimo casa: "+self.email
        self.br.form["opening_balance"] = str(randint(50000, 100000))
        self.br.form["opening_balance_date"] = "2010-03-01"
        self.br.form["interest"] = "6"
        self.br.submit()

    def enter_categories(self):
        for link in self.br.links():
            if link.text == "Categories":
                self.br.follow_link(link)
                break

    def create_categories(self):
        categories = ["Roupa: ", "Comida: ", "Carro: ", "Mobilia: ", "Eletrodomésticos: "]

        for c in categories:
            for link in self.br.links():
                if c == "Roupa":
                    if link.text == "Create a category":
                        self.br.follow_link(link)
                else:
                    if link.text == "New category":
                        self.br.follow_link(link)

            self.br.select_form(nr=1)
            self.br.form["name"] = c+self.email
            self.br.submit()

    def enter_transactions_expenses(self):
        for link in self.br.links():
            if link.text == "Expenses":
                self.br.follow_link(link)
                break

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
        requests.get(url=self.base_url+"/api/v1/preferences", headers=self.api_headers).json()

    def create_transactions_expenses(self):
        user_id = 0
        categories = ["Roupa: ", "Comida: ", "Carro: ", "Mobilia: ", "Eletrodomésticos: "]
        users = requests.get(url=self.base_url+"/api/v1/users", headers=self.api_headers).json()
        for u in users["data"]:
            if u["attributes"]["email"] == self.email:
                user_id = u["id"]
                break

        for i in range(0, 10):
            id = randint(0, 4)
            transaction = { "type": "withdrawal",
                            "date": "2020-03-0"+str(randint(1, 31)),
                            "amount": str(randint(5, 30)),
                            "description": "Expenses",
                            "source_name": "Conta Corrente: "+self.email,
                            "destination_name": "Supermercado: "+self.email,
                            "category_name": categories[id]+self.email
                            }
            data = {
                "user": user_id,
                "transactions": [transaction]
            }
            requests.post(
                url=self.base_url+"/api/v1/transactions",
                data=json.dumps(data),
                headers=self.api_headers
            ).json()

    def enter_transactions_revenue(self):
        for link in self.br.links():
            if link.text == "Revenue / income":
                self.br.follow_link(link)
                break

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
        requests.get(url=self.base_url+"/api/v1/preferences/transaction_journal_optional_fields",
                     headers=self.api_headers).json()

    def create_transactions_revenue(self):
        user_id = 0

        users = requests.get(url=self.base_url+"/api/v1/users", headers=self.api_headers).json()
        for u in users["data"]:
            if u["attributes"]["email"] == self.email:
                user_id = u["id"]
                break

        transaction = { "type": "deposit",
                        "date": "2020-03-01",
                        "amount": "1000",
                        "description": "Salary",
                        "source_name": "Empregador: "+self.email,
                        "destination_name": "Conta Corrente: "+self.email,
                        }
        data = {
            "user": user_id,
            "transactions": [transaction]
        }

        requests.post(
            url=self.base_url+"/api/v1/transactions",
            data=json.dumps(data),
            headers=self.api_headers
        ).json()

    def enter_reports(self):
        for link in self.br.links():
            if link.text == "Reports":
                self.br.follow_link(link)
                break

    def load_reports(self):
        requests.get(self.base_url + "/reports/options/audit", cookies=self.browser_cookies).json()

    def enter_month_balance(self):
        for link in self.br.links():
            if link.text == "Last month, all accounts":
                self.br.follow_link(link)
                break

        return self.br.geturl().split("/")[5]

    def load_month_balance(self, id):
        requests.get(self.base_url + "/report-data/account/general/"+id+"/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/income/"+id+"/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/expenses/"+id+"/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/operations/"+id+"/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/bill/overview/"+id+"/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/chart/account/report/"+id+"/20200301/20200331",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/report-data/budget/general/"+id+"/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/balance/general/"+id+"/20200301/20200331",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/category/operations/"+id+"/20200301/20200331",
                     cookies=self.browser_cookies)

    def enter_year_balance(self):
        for link in self.br.links():
            if link.text == "Current year, all accounts":
                self.br.follow_link(link)
                break

        return self.br.geturl().split("/")[5]

    def load_year_balance(self, id):
        requests.get(self.base_url + "/report-data/account/general/"+id+"/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/income/"+id+"/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/expenses/"+id+"/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/operations/operations/"+id+"/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/reports/default/"+id+"/currentYearStart/currentYearEnd",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/chart/report/net-worth/"+id+"/20200101/20201231",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/chart/report/operations/"+id+"/20200101/20201231",
                     cookies=self.browser_cookies).json()
        requests.get(self.base_url + "/report-data/budget/period/"+id+"/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/category/expenses/"+id+"/20200101/20201231",
                     cookies=self.browser_cookies)
        requests.get(self.base_url + "/report-data/category/income/"+id+"/20200101/20201231",
                     cookies=self.browser_cookies)



