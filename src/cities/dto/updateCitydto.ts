import{ IsString } from "class-validator";

export class UpdateCityDto{
    @IsString({message: 'Insira uma cidade válida'})
    name : string;

    @IsString({message: 'Insira um estado válido'})
    state: string;
}