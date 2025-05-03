import { ApiProperty } from '@nestjs/swagger';

export class Transaction {
  @ApiProperty()
  id: number;

  @ApiProperty()
  bankStatementId: number;

  @ApiProperty()
  description: string;

  @ApiProperty()
  amount: number;

  @ApiProperty()
  date: Date;

  @ApiProperty()
  createdAt: Date;

  @ApiProperty()
  updatedAt: Date;

  // Add more fields as needed
}
