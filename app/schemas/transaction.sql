CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    balance REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bank_statement_id INTEGER,
    FOREIGN KEY (bank_statement_id) REFERENCES bank_statements (id) ON
DELETE CASCADE
);