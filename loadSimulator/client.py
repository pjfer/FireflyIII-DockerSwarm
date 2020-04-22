import mechanize

from ApiCalls import ApiClient

BASE_URL = "http://localhost:8001"
REDIRECT_URI = 'https://google.com'
AUTHORIZE_URL = "http://0.0.0.0:8001/oauth/authorize"
ACCESS_TOKEN_URL = "http://0.0.0.0:8001/oauth/token"

client_id = 18
client_secret = "mHWqU6PkjY0XiuARD017f6q0py9FJkVq4u2GGZOo"


def lifecycle(email, pw, base_url, client_id, client_secret, redirect_uri, authorize_url, access_token_url):
    cli = ApiClient(email, pw, base_url, client_id, client_secret,  redirect_uri, authorize_url,
                    access_token_url, "rafael@ua.pt", "c_P2+1D1.6ie3Uz%1Y1")

    #cli.login()
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





lifecycle("user1@mail.com", "?URz/cJqyL3b)=DQ", BASE_URL, client_id, client_secret,
          REDIRECT_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL)
