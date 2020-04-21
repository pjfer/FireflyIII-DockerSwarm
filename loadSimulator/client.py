import mechanize

from ApiCalls import ApiClient

BASE_URL = "http://localhost:8001"
REDIRECT_URI = 'http://0.0.0.0:8001/new-user'
AUTHORIZE_URL = "http://0.0.0.0:8001/oauth/authorize"
ACCESS_TOKEN_URL = "http://0.0.0.0:8001/oauth/token"

client_id = 3
client_secret = "6Eb11vg04jHsCcYeOCCtREF6LX7TRRkYgxtA7vlG"


def lifecycle(email, pw, base_url, client_id, client_secret, redirect_uri, authorize_url, access_token_url):
    cli = ApiClient(email, pw, base_url, client_id, client_secret,  redirect_uri, authorize_url, access_token_url)

    cli.login()  # Realiza o login
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





lifecycle("trashuserzths@protonmail.com", "qwerty1234", BASE_URL, client_id, client_secret,
          REDIRECT_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL)
