import { Injectable, Res } from '@nestjs/common';
import { CreateBankStatementDto } from './dto/create-bank-statement.dto';
import { UpdateBankStatementDto } from './dto/update-bank-statement.dto';
import { Response } from 'express';

@Injectable()
export class BankStatementsService {
  // In-memory storage for demonstration
  private bankStatements = [];
  private transactions = [];
  private idCounter = 1;

  upload(file: Express.Multer.File) {
    // Simulate extracting transactions and saving bank statement
    const bankStatement = {
      id: this.idCounter++,
      fileName: file.originalname,
      createdAt: new Date(),
      updatedAt: new Date(),
      amount: 0,
    };
    this.bankStatements.push(bankStatement);
    // Simulate extracting transactions (empty for now)
    return bankStatement;
  }

  findAll(query: any) {
    let result = [...this.bankStatements];
    // Filtering
    if (query.q) {
      result = result.filter((bs) => bs.fileName.includes(query.q));
    }
    if (query.dateFrom) {
      result = result.filter(
        (bs) => new Date(bs.createdAt) >= new Date(query.dateFrom),
      );
    }
    if (query.dateTo) {
      result = result.filter(
        (bs) => new Date(bs.createdAt) <= new Date(query.dateTo),
      );
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
    return this.bankStatements.find((bs) => bs.id === id);
  }

  downloadPdf(id: number, res: Response) {
    // Placeholder: send a dummy PDF
    res.setHeader('Content-Type', 'application/pdf');
    res.send(
      Buffer.from('%PDF-1.4\n%Dummy PDF file for bank statement\n', 'utf-8'),
    );
  }

  update(id: number, updateBankStatementDto: UpdateBankStatementDto) {
    const bs = this.bankStatements.find((bs) => bs.id === id);
    if (bs) {
      Object.assign(bs, updateBankStatementDto, { updatedAt: new Date() });
    }
    return bs;
  }

  remove(id: number) {
    // Remove bank statement
    this.bankStatements = this.bankStatements.filter((bs) => bs.id !== id);
    // Remove associated transactions
    this.transactions = this.transactions.filter(
      (t) => t.bankStatementId !== id,
    );
    return { deleted: true };
  }
}
