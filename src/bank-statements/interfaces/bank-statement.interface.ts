import { Transaction } from 'src/transactions/interfaces/transaction.interface';

export interface BankStatement {
  id: number;
  date: Date;
  accountNumber: string;
  totalPages: number;
  branch: string;
  beginningBalance: number;
  endingBalance: number;
  totalDebit: number;
  totalCredit: number;
  createdAt: Date;
  updatedAt: Date;
  userId: number;
  transactions: Transaction[];
}

export interface BankStatementQuery {
  q?: string;
  dateFrom?: string;
  dateTo?: string;
  sort?: string;
  offset?: number;
  limit?: number;
}

export interface BankStatementFilter {
  q?: string;
  dateFrom?: string;
  dateTo?: string;
  sort?: string;
  offset?: number;
  limit?: number;
  userId?: number;
  bankStatementId?: number;
  transactionId?: number;
  transactionDateFrom?: string;
  transactionDateTo?: string;
  transactionSort?: string;
  transactionOffset?: number;
  transactionLimit?: number;
  transactionQ?: string;
  transactionBankStatementId?: number;
}
