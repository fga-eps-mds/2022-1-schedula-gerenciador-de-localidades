import { Test, TestingModule } from '@nestjs/testing';
import { CitiesController } from './cities.controller';
import { CitiesService } from './cities.service';
import { v4 as uuidv4 } from 'uuid';
import { CreateCityDto } from './dto/createCitydto';
import { UpdateCityDto } from './dto/updateCitydto';

describe('CitiesController', () => {
  let citiesController: CitiesController;

  const mockUuid = uuidv4();

  const mockCreateCityDto: CreateCityDto = {
    name: 'mock_city',
    state: 'GO',
  };

  const mockUpdteCityDto: UpdateCityDto = {
    name: 'new_mock_city',
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

    citiesController = module.get<CitiesController>(CitiesController);
  });

  it('should be defined', () => {
    expect(citiesController).toBeDefined();
  });

  it('should create a new city with success', async () => {
    const dto = mockCreateCityDto;
    const response = await citiesController.createCity(dto);

    expect(response).toMatchObject({ ...dto });
  });

  it('should return an city with success', async () => {
    const cityId = mockUuid;
    const response = await citiesController.findCityById(cityId);

    expect(response).toMatchObject({ id: cityId });
  });

  it('should return all cities with success', async () => {
    const response = await citiesController.findCities();

    expect(response.length).toBeGreaterThan(0);
    expect(response).toEqual([{ ...mockCreateCityDto }]);
  });

  it('should update an city with success', async () => {
    const cityId = mockUuid;
    const dto = mockUpdteCityDto;
    const response = await citiesController.updateCity(dto, cityId);

    expect(response).toMatchObject({ ...dto, id: cityId });
  });

  it('should delete an city with success', async () => {
    const cityId = mockUuid;
    const successMessage = 'Cidade removida com sucesso';
    const response = await citiesController.deleteCity(cityId);

    expect(response).toMatchObject({ message: successMessage });
  });
});
