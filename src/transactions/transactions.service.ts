import { Injectable } from '@nestjs/common';
import { CreateTransactionDto } from './dto/create-transaction.dto';
import { UpdateTransactionDto } from './dto/update-transaction.dto';

@Injectable()
export class TransactionsService {
  // In-memory storage for demonstration
  private transactions = [];
  private idCounter = 1;

  create(createTransactionDto: CreateTransactionDto) {
    const transaction = {
      id: this.idCounter++,
      ...createTransactionDto,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.transactions.push(transaction);
    return transaction;
  }

  findAll(query: any) {
    let result = [...this.transactions];
    // Filtering
    if (query.q) {
      result = result.filter(
        (t) => t.description && t.description.includes(query.q),
      );
    }
    if (query.bankStatementId) {
      result = result.filter((t) => t.bankStatementId == query.bankStatementId);
    }
    if (query.dateFrom) {
      result = result.filter(
        (t) => new Date(t.date) >= new Date(query.dateFrom),
      );
    }
    if (query.dateTo) {
      result = result.filter((t) => new Date(t.date) <= new Date(query.dateTo));
    }
    // Sorting
    if (query.sort) {
      const sortKey = query.sort.replace('-', '');
      const desc = query.sort.startsWith('-');
      result = result.sort((a, b) => {
        if (a[sortKey] < b[sortKey]) return desc ? 1 : -1;
        if (a[sortKey] > b[sortKey]) return desc ? -1 : 1;
        return 0;
      });
    }
    // Pagination
    const offset = Number(query.offset) || 0;
    const limit = Number(query.limit) || 10;
    return result.slice(offset, offset + limit);
  }

  findOne(id: number) {
    return this.transactions.find((t) => t.id === id);
  }

  update(id: number, updateTransactionDto: UpdateTransactionDto) {
    const t = this.transactions.find((t) => t.id === id);
    if (t) {
      Object.assign(t, updateTransactionDto, { updatedAt: new Date() });
    }
    return t;
  }

  remove(id: number) {
    this.transactions = this.transactions.filter((t) => t.id !== id);
    return { deleted: true };
  }
}
