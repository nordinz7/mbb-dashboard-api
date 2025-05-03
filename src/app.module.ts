import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { BankStatementsModule } from './bank-statements/bank-statements.module';
import { TransactionsModule } from './transactions/transactions.module';

@Module({
  imports: [BankStatementsModule, TransactionsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
