# mbb-dashboard-api

# Flow

1. User uploads a bank statement.
2. The system processes the bank statement and extracts transactions.
3. The system stores the transactions in the database.
4. The user can view the transactions through the API.
5. The user can filter transactions by date range, bank statement ID, and sort order.
6. The user can delete a bank statement, which also deletes the associated transactions.
7. The user can view the details of a specific transaction.

# API Endpoints

## Bank Statements

- **POST** `/api/bank-statements/upload`

- **GET** `/api/bank-statements`

  - Query Parameters:
    - `q=search term`
    - `date_from=YYYY-MM-DD`
    - `date_to=YYYY-MM-DD`
    - `limit=10`
    - `offset=0`
    - `sort=-createdAt` prefix - means DESC
    - `sort=updatedAt` prefix - means DESC
    - `sort=amount`

- **GET** `/api/bank-statements/:id`

  - Query Parameters:
    - `download=true`

- **DELETE** `/api/bank-statements/:id`

---

## Transactions

- **GET** `/api/transactions`

  - Query Parameters:
    - `q=search term`
    - `bank_statement_id=123`
    - `date_from=YYYY-MM-DD`
    - `date_to=YYYY-MM-DD`
    - `limit=10`
    - `offset=0`
    - `sort=createdAt`
    - `sort=amount`

- **GET** `/api/transactions/:id`
