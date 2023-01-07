import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Post,
  Put,
} from '@nestjs/common';
import { CitiesService } from './cities.service';
import { City } from './city.entity';
import { CreateCityDto } from './dto/createCitydto';
import { UpdateCityDto } from './dto/updateCitydto';

@Controller('cities')
export class CitiesController {
  constructor(private citiesService: CitiesService) {}

  @Get()
  async findCities(): Promise<City[]> {
    return await this.citiesService.findCities();
  }

  @Get(':id')
  async findCityById(@Param('id') id: string): Promise<City> {
    return await this.citiesService.findCityById(id);
  }

  @Post()
  async createCity(@Body() dto: CreateCityDto): Promise<City> {
    return await this.citiesService.createCity(dto);
  }

  @Put(':id')
  async updateCity(
    @Body() dto: UpdateCityDto,
    @Param('id') id: string,
  ): Promise<City> {
    return await this.citiesService.updateCity(dto, id);
  }

  @Delete(':id')
  async deleteCity(@Param('id') id: string) {
    await this.citiesService.deleteCity(id);
    return {
      message: 'Cidade removida com sucesso',
    };
  }
}
