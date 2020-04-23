import json
from ApiCalls import ApiClient

BASE_URL = "http://localhost:8001"
REDIRECT_URI = 'https://google.com'
AUTHORIZE_URL = "http://0.0.0.0:8001/oauth/authorize"
ACCESS_TOKEN_URL = "http://0.0.0.0:8001/oauth/token"

credentials_file = open("credentials.json", "a+")

def lifecycle(file, email, pw, base_url, redirect_uri, authorize_url, access_token_url, client_id=None, client_secret=None):

    if client_id is None:
        cli = ApiClient(base_url, redirect_uri, authorize_url, access_token_url, email, pw)
        cli.load_dashboard_resources()  # Obtém os diferentes recursos presentes na dashboard (simular carga)
        cli.enter_assets()
        cli.create_asset_account()
        cli.enter_expenses()
        cli.create_expense_account()
        cli.enter_revenue()
        cli.create_revenue_account()
        cli.enter_liabilities()
        cli.create_liability()
        cli.enter_categories()
        cli.create_categories()
        credentials = cli.get_api_credentias()
        line = json.dumps({"email": email, "client_id": credentials[0], "client_secret": credentials[1]})
        file.write(line+"\n")
    else:
        cli = ApiClient(base_url, redirect_uri, authorize_url, access_token_url, email, pw,
                        client_id=client_id, client_secret=client_secret)
        cli.login()

    cli.enter_transactions_expenses()
    cli.load_transactions_expenses()
    cli.create_transactions_expenses()
    cli.enter_transactions_revenue()
    cli.load_transactions_revenue()
    cli.create_transactions_revenue()
    cli.enter_reports()
    cli.load_reports()
    temp = cli.enter_month_balance()
    cli.load_month_balance(temp)
    cli.enter_reports()
    cli.load_reports()
    temp = cli.enter_year_balance()
    cli.load_year_balance(temp)


def main():
    f = open("credentials.json", "r")
    credentials = {}
    for line in f:
        c = json.loads(line)
        credentials[c["email"]] = (c["client_id"], c["client_secret"])
    f.close()

    email = "rafael@ua.pt"
    pw = "?URz/cJqyL3b)=DQ"

    if email in credentials:
        lifecycle(email, pw, BASE_URL, REDIRECT_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL,
                  client_id=credentials[email][0], client_secret=credentials[email][1])
    else:
        lifecycle(credentials_file, email, pw, BASE_URL, REDIRECT_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL)
    credentials_file.close()


main()