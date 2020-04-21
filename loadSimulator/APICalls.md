# API Calls
## Calls DashBoard
### Call Base
- http://localhost:8001/

### Calls extra
- http://localhost:8001/chart/account/frontpage
- http://localhost:8001/chart/bill/frontpage
- http://localhost:8001/chart/budget/frontpage
- http://localhost:8001/chart/category/frontpage
- http://localhost:8001/chart/account/expense
- http://localhost:8001/chart/account/revenue
- http://localhost:8001/json/box/balance
- http://localhost:8001/json/box/bills
- http://localhost:8001/json/box/available
- http://localhost:8001/json/box/net-worth
- http://localhost:8001/json/frontpage/piggy-banks

## Accounts
### Assets - Create Assets
#### Call base
- http://localhost:8001/accounts/asset ( Entrar nos assets )
- http://localhost:8001/accounts/create/asset (Criar conta de assets)

#### Calls Extra
 - Não pede calls extra

### Assets - Expense Assets
#### Call base
- http://localhost:8001/accounts/expense ( Entrar nos expenses )
- http://localhost:8001/accounts/create/expense ( Criar conta de expenses )

#### Calls Extra
 - Não pede calls extra

### Assets - Revenue Assets
#### Call base
- http://localhost:8001/accounts/revenue ( Entrar nos revenue )
- http://localhost:8001/accounts/create/expense ( Criar conta de revenue )

#### Calls Extra
 - Não pede calls extra

### Assets - Liabilities Assets
#### Call base
- http://localhost:8001/accounts/liabilities ( Entrar nas liabilities )
- http://localhost:8001/accounts/create/liabilities ( Criar conta de liability )

#### Calls Extra
 - Não pede calls extra

## Categories
### Call base
- http://localhost:8001/categories (Entrar nas categorias)
- http://localhost:8001/categories/create (Cria categoria)

### Calls Extra
- Não pede calls extra.

## Transactions
### Expenses

#### Call Base
- http://localhost:8001/transactions/withdrawal (Entra nas withdraws)
- http://localhost:8001/transactions/create/withdrawal (Criar withdraw)

#### Calls Extra
- http://localhost:8001/chart/transactions/categories/withdrawal/2020-04-01/2020-04-30 (Entra nas withdraws)
- http://localhost:8001/chart/transactions/budgets/2020-04-01/2020-04-30 (Entra nas withdraws)
- http://localhost:8001/chart/transactions/destinationAccounts/withdrawal/2020-04-01/2020-04-30 (Entra nas withdraws)
- http://localhost:8001/json/currencies (Criar withdraw)
- http://localhost:8001/json/budgets (Criar withdraw)
- http://localhost:8001/json/piggy-banks (Criar withdraw)
- http://localhost:8001/api/v1/preferences (Criar withdraw)

### Revenue
#### Call base
- http://localhost:8001/transactions/deposit (Entra nas revenues)
- http://localhost:8001/transactions/create/deposit (Criar revenue)

#### Call Extra
- http://localhost:8001/chart/transactions/categories/deposit/2020-04-01/2020-04-30 (Entra nas revenues)
- http://localhost:8001/chart/transactions/destinationAccounts/deposit/2020-04-01/2020-04-30 (Entra nas revenues)
- http://localhost:8001/chart/transactions/sourceAccounts/deposit/2020-04-01/2020-04-30 (Entra nas revenues)
- http://localhost:8001/json/currencies (Criar revenue)
- http://localhost:8001/json/budgets (Criar revenue)
- http://localhost:8001/json/piggy-banks (Criar revenue)
- http://localhost:8001/api/v1/preferences/transaction_journal_optional_fields (Criar revenue)

## Reports
### Call base
- http://localhost:8001/reports (Entra nos reports)
- http://localhost:8001/reports/default/4,1,3,9/currentMonthStart/currentMonthEnd (Balanço Mensal [quick link])
- http://localhost:8001/reports/default/4,1,3,9/currentYearStart/currentYearEnd (Balanço Anual [quick link])

### Calls Extra
- http://localhost:8001/reports/options/audit (Entra nos Reports)
- http://localhost:8001/report-data/operations/expenses/4,1,3,9/20200401/20200430 (Balanço Mensal)
- http://localhost:8001/report-data/operations/operations/4,1,3,9/20200401/20200430 (Balanço Mensal)
- http://localhost:8001/report-data/bill/overview/4,1,3,9/20200401/20200430 (Balanço Mensal)
- http://localhost:8001/chart/account/report/4,1,3,9/20200401/20200430 (Balanço Mensal)
- http://localhost:8001/report-data/category/operations/4,1,3,9/20200401/20200430 (Balanço Mensal)
- http://localhost:8001/report-data/budget/general/4,1,3,9/20200401/20200430 (Balanço Mensal)
- http://localhost:8001/report-data/balance/general/4,1,3,9/20200401/20200430 (Balanço Mensal)
- http://localhost:8001/report-data/account/general/4,1,3,9/20200401/20200430 (Balanço Mensal)
- http://localhost:8001/report-data/operations/income/4,1,3,9/20200401/20200430 (Balanço Mensal)
- http://localhost:8001/report-data/account/general/4,1,3,9/20200101/20201231 (Balanço Anual)
- http://localhost:8001/report-data/operations/income/4,1,3,9/20200101/20201231 (Balanço Anual)
- http://localhost:8001/report-data/operations/expenses/4,1,3,9/20200101/20201231 (Balanço Anual)
- http://localhost:8001/report-data/operations/operations/4,1,3,9/20200101/20201231 (Balanço Anual)
- http://localhost:8001/reports/default/4,1,3,9/currentYearStart/currentYearEnd (Balanço Anual)
- http://localhost:8001/chart/report/net-worth/4,1,3,9/20200101/20201231 (Balanço Anual)
- http://localhost:8001/chart/report/operations/4,1,3,9/20200101/20201231 (Balanço Anual)
- http://localhost:8001/report-data/budget/period/4,1,3,9/20200101/20201231 (Balanço Anual)
- http://localhost:8001/report-data/category/expenses/4,1,3,9/20200101/20201231 (Balanço Anual)
- http://localhost:8001/report-data/category/income/4,1,3,9/20200101/20201231 (Balanço Anual)























