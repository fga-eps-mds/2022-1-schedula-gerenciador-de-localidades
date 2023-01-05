import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CitiesController } from './cities.controller';
import { CitiesService } from './cities.service';
import { City } from './city.entity';
import { CreateCityDto } from './dto/createCitydto';

describe('CitiesService', () => {
  let citiesService: CitiesService;
  let citiesRepository: Repository<City>;

  const mockCityDto: CreateCityDto = {
    name: 'Test Name',
    state: 'DF',
  };

  const citiesEntityList = [{ ...mockCityDto }];

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        CitiesService,
        {
          provide: getRepositoryToken(City),
          useValue: {
            create: jest.fn().mockResolvedValue(new City()),
            find: jest.fn().mockResolvedValue(citiesEntityList),
            findOne: jest.fn().mockResolvedValue(citiesEntityList[0]),
            update: jest.fn(),
            delete: jest.fn(),
          },
        },
      ],
      controllers: [CitiesController],
    }).compile();

    citiesService = module.get<CitiesService>(CitiesService);
    citiesRepository = module.get<Repository<City>>(getRepositoryToken(City));
  });

  it('should be defined', () => {
    expect(citiesService).toBeDefined();
    expect(citiesRepository).toBeDefined();
  });
});
