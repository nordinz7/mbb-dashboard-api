import { PartialType } from '@nestjs/mapped-types';
import { CreateBankStatementDto } from './create-bank-statement.dto';

export class UpdateBankStatementDto extends PartialType(CreateBankStatementDto) {}
