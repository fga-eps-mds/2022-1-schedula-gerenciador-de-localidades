import { IsNotEmpty, IsString } from 'class-validator';

export class CreateCityDto {
  @IsNotEmpty({ message: 'Insira uma cidade' })
  @IsString({ message: 'Insira uma cidade válida' })
  name: string;

  @IsNotEmpty({ message: 'Insira um estado' })
  @IsString({ message: 'Insira um estado válido' })
  state: string;
}
