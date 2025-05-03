import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  Query,
  UploadedFile,
  UseInterceptors,
  Res,
} from '@nestjs/common';
import { BankStatementsService } from './bank-statements.service';
import { CreateBankStatementDto } from './dto/create-bank-statement.dto';
import { UpdateBankStatementDto } from './dto/update-bank-statement.dto';
import { FileInterceptor } from '@nestjs/platform-express';
import { Response } from 'express';

@Controller('bank-statements')
export class BankStatementsController {
  constructor(private readonly bankStatementsService: BankStatementsService) {}

  @Post('upload')
  @UseInterceptors(FileInterceptor('file'))
  upload(@UploadedFile() file: Express.Multer.File) {
    // Placeholder: process file and extract transactions
    return this.bankStatementsService.upload(file);
  }

  @Get()
  findAll(
    @Query('q') q?: string,
    @Query('date_from') dateFrom?: string,
    @Query('date_to') dateTo?: string,
    @Query('limit') limit?: number,
    @Query('offset') offset?: number,
    @Query('sort') sort?: string,
  ) {
    return this.bankStatementsService.findAll({
      q,
      dateFrom,
      dateTo,
      limit,
      offset,
      sort,
    });
  }

  @Get(':id')
  findOne(
    @Param('id') id: string,
    @Query('download') download?: string,
    @Res() res?: Response,
  ) {
    if (download === 'true') {
      // Placeholder: return PDF file
      return this.bankStatementsService.downloadPdf(+id, res);
    }
    return this.bankStatementsService.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateBankStatementDto: UpdateBankStatementDto,
  ) {
    return this.bankStatementsService.update(+id, updateBankStatementDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.bankStatementsService.remove(+id);
  }
}
