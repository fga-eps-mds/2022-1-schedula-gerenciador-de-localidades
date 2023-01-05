import { Test, TestingModule } from '@nestjs/testing';
import { CitiesController } from './cities.controller';
import { CitiesService } from './cities.service';
import { CreateCityDto } from './dto/createCitydto';

describe('CitiesController', () => {
  let controller: CitiesController;

  const mockCreateCityDto: CreateCityDto = {
    name: 'mock_city',
    state: 'GO',
  };

  const mockCitiesService = {
    createCity: jest.fn((dto) => {
      return {
        ...dto,
      };
    }),
    findCityById: jest.fn((id) => {
      return {
        ...mockCreateCityDto,
        id,
      };
    }),
    updateCity: jest.fn((dto, id) => {
      return {
        ...mockCreateCityDto,
        ...dto,
        id,
      };
    }),
    deleteCity: jest.fn((id) => {
      return;
    }),
    findCities: jest.fn(() => {
      return [{ ...mockCreateCityDto }];
    }),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [CitiesController],
      providers: [CitiesService],
    })
      .overrideProvider(CitiesService)
      .useValue(mockCitiesService)
      .compile();

    controller = module.get<CitiesController>(CitiesController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
