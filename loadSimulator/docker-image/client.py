import json
import sys
import time
from random import randint
import os.path
from ApiCalls import ApiClient

BASE_URL = "http://10.2.0.1:40100"
REDIRECT_URI = 'https://google.com'
AUTHORIZE_URL = "http://10.2.0.1:40100/oauth/authorize"
ACCESS_TOKEN_URL = "http://10.2.0.1:40100/oauth/token"


def lifecycle(email, pw, base_url, redirect_uri, authorize_url, access_token_url, client_id=None, client_secret=None, file=None):

    if client_id is None:
        cli = ApiClient(base_url, redirect_uri, authorize_url, access_token_url, email, pw)
        cli.load_dashboard_resources()  # Obtém os diferentes recursos presentes na dashboard (simular carga)
        print("Client created")
        credentials = cli.get_api_credentias()
        line = json.dumps({"email": email, "client_id": credentials[0], "client_secret": credentials[1]})
        file.write(line+"\n")
        time.sleep(randint(1, 5))
        cli.enter_assets()
        time.sleep(randint(1, 5))
        cli.create_asset_account()
        time.sleep(randint(1, 5))
        cli.enter_expenses()
        time.sleep(randint(1, 5))
        cli.create_expense_account()
        time.sleep(randint(1, 5))
        cli.enter_revenue()
        time.sleep(randint(1, 5))
        cli.create_revenue_account()
        time.sleep(randint(1, 5))
        cli.enter_liabilities()
        time.sleep(randint(1, 5))
        cli.create_liability()
        time.sleep(randint(1, 5))
        print("Accounts created")
        cli.enter_categories()
        time.sleep(randint(1, 5))
        cli.create_categories()
        print("Categories created")
        time.sleep(randint(1, 5))
    else:
        cli = ApiClient(base_url, redirect_uri, authorize_url, access_token_url, email, pw,
                        client_id=client_id, client_secret=client_secret)
        cli.login()
        cli.load_dashboard_resources()
        print("Client logged in")
        time.sleep(randint(1, 5))

    cli.enter_transactions_expenses()
    cli.load_transactions_expenses()
    time.sleep(randint(1, 5))
    cli.create_transactions_expenses()
    print("Expenses transactions created")
    time.sleep(randint(1, 5))
    cli.enter_transactions_revenue()
    cli.load_transactions_revenue()
    print("Revenue transaction created")
    time.sleep(randint(1, 5))
    cli.create_transactions_revenue()
    time.sleep(randint(1, 5))
    cli.enter_reports()
    cli.load_reports()
    print("Enter the Reports")
    time.sleep(randint(1, 5))
    temp = cli.enter_month_balance()
    cli.load_month_balance(temp)
    time.sleep(randint(1, 5))
    cli.enter_reports()
    cli.load_reports()
    time.sleep(randint(1, 5))
    temp = cli.enter_year_balance()
    cli.load_year_balance(temp)
    time.sleep(randint(1, 5))
    print("Client lifecycle ended.")


def main(email, pw):

    if os.path.isfile("data/credentials/"+email.split("@")[0]+".json"):
        f = open("data/credentials/"+email.split("@")[0]+".json", "r")
        credentials = json.load(f)
        lifecycle(email, pw, BASE_URL, REDIRECT_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL,
                  client_id=credentials["client_id"], client_secret=credentials["client_secret"])
    else:
        f = open("data/credentials/"+email.split("@")[0]+".json", "w")
        lifecycle(email, pw, BASE_URL, REDIRECT_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL, file=f)
        f.close()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
