import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { BankStatementsModule } from './bank-statements/bank-statements.module';
import { TransactionsModule } from './transactions/transactions.module';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [
    BankStatementsModule,
    TransactionsModule,
    // eslint-disable-next-line @typescript-eslint/no-unsafe-call
    TypeOrmModule.forRoot({
      type: 'sqlite',
      // host: 'localhost',
      // port: 3306,
      // username: 'root',
      // password: 'root',
      database: 'test',
      entities: [],
      synchronize: false, // Set to true in development only
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
