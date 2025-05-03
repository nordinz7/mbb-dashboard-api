export class CreateTransactionDto {
  bankStatementId: number;
  description: string;
  amount: number;
  date: Date;
  // Add more fields as needed
}
