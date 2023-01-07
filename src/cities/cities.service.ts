import {
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { City } from './city.entity';
import { CreateCityDto } from './dto/createCitydto';
import { UpdateCityDto } from './dto/updateCitydto';

@Injectable()
export class CitiesService {
  constructor(
    @InjectRepository(City)
    private cityRepo: Repository<City>,
  ) {}

  async createCity(dto: CreateCityDto): Promise<City> {
    const city = this.cityRepo.create({ ...dto });
    try {
      return await this.cityRepo.save(city);
    } catch (error) {
      throw new InternalServerErrorException(error.message);
    }
  }

  async findCities(): Promise<City[]> {
    const cities = await this.cityRepo.find();

    if (cities.length === 0) {
      throw new NotFoundException('Não existem cidades cadastradas');
    }
    return cities;
  }

  async findCityById(idCity: string) {
    const city = await this.cityRepo.findOneBy({ id: idCity });
    if (!city) {
      throw new NotFoundException('Não foi possível encontrar esta cidade');
    }
    return city;
  }

  async updateCity(dto: UpdateCityDto, idCity: string): Promise<City> {
    const { name, state } = dto;
    const city = await this.cityRepo.findOneBy({ id: idCity });

    try {
      city.name = name;
      city.state = state;

      await this.cityRepo.save(city);
      return city;
    } catch (error) {
      throw new InternalServerErrorException(error.message);
    }
  }

  async deleteCity(idCity: string) {
    const result = await this.cityRepo.delete({ id: idCity });
    if (!result) throw new NotFoundException('Cidade não encontrada');
    if (result.affected === 0) {
      throw new NotFoundException('Não foi encontrada uma cidade com este id');
    }
  }
}
