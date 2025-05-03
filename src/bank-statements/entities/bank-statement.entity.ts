import { ApiProperty } from '@nestjs/swagger';

export class BankStatement {
  @ApiProperty()
  id: number;

  @ApiProperty()
  fileName: string;

  @ApiProperty()
  createdAt: Date;

  @ApiProperty()
  updatedAt: Date;

  @ApiProperty()
  amount: number;

  // Add more fields as needed
}
