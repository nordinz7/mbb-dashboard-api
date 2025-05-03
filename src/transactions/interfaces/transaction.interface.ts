export interface Transaction {
  id: number;
  statementId: number;
  date: Date;
  desc: string;
  amt: number;
  bal: number;
  createdAt: Date;
  updatedAt: Date;
}
