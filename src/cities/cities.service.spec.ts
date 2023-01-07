import {
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { DeleteResult, Repository } from 'typeorm';
import { v4 as uuid } from 'uuid';
import { CitiesService } from './cities.service';
import { City } from './city.entity';
import { CreateCityDto } from './dto/createCitydto';
import { UpdateCityDto } from './dto/updateCitydto';

describe('CitiesService', () => {
  let citiesService: CitiesService;
  let citiesRepository: Repository<City>;

  const mockUuid = uuid();

  const mockCityDto: CreateCityDto = {
    name: 'Test Name',
    state: 'DF',
  };

  const mockUpdateCityDto: UpdateCityDto = {
    name: 'Test Name Updated',
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
            findOneBy: jest.fn().mockResolvedValue(citiesEntityList[0]),
            update: jest.fn(),
            delete: jest.fn(),
            save: jest.fn(),
          },
        },
      ],
    }).compile();

    citiesService = module.get<CitiesService>(CitiesService);
    citiesRepository = module.get<Repository<City>>(getRepositoryToken(City));
  });

  it('should be defined', () => {
    expect(citiesService).toBeDefined();
    expect(citiesRepository).toBeDefined();
  });

  describe('createCity', () => {
    const dto = mockCityDto;
    it('should call city repository with correct params', async () => {
      await citiesService.createCity(dto);
      expect(citiesRepository.create).toHaveBeenCalledWith({
        ...dto,
      });
      expect(citiesRepository.create);
    });

    it('should return an internal error exception', async () => {
      jest.spyOn(citiesRepository, 'save').mockRejectedValue(new Error());

      expect(citiesService.createCity(mockCityDto)).rejects.toThrowError(
        InternalServerErrorException,
      );
    });
  });

  describe('findCities', () => {
    it('should return a city entity list successfully', async () => {
      const response = await citiesService.findCities();

      expect(response).toEqual(citiesEntityList);
      expect(citiesRepository.find).toHaveBeenCalledTimes(1);
    });

    it('should throw a not found exception', () => {
      jest.spyOn(citiesRepository, 'find').mockResolvedValueOnce([]);

      expect(citiesService.findCities()).rejects.toThrowError(
        NotFoundException,
      );
    });
  });

  describe('findCityById', () => {
    const id = mockUuid;

    it('should return an city entity successfully', async () => {
      const response = await citiesService.findCityById(id);

      expect(response).toEqual(citiesEntityList[0]);
    });

    it('should throw a not found exception', () => {
      jest.spyOn(citiesRepository, 'findOneBy').mockResolvedValueOnce(null);

      expect(citiesService.findCityById(id)).rejects.toThrowError(
        NotFoundException,
      );
    });
  });

  describe('updateCity', () => {
    const id = mockUuid;
    const dto = mockUpdateCityDto;

    it('should return an updated city successfully', async () => {
      const response = await citiesService.updateCity({ ...dto }, id);
      expect(response).toMatchObject({ ...mockUpdateCityDto });
    });

    it('should return an internal server error exception when city cannot be updated', async () => {
      jest.spyOn(citiesRepository, 'save').mockRejectedValue(new Error());

      expect(citiesService.updateCity({ ...dto }, id)).rejects.toThrowError(
        InternalServerErrorException,
      );
    });
  });

  describe('deleteCity', () => {
    it('should return a not found exception', () => {
      const id = mockUuid;

      jest.spyOn(citiesRepository, 'delete').mockResolvedValue(null);
      expect(citiesService.deleteCity(id)).rejects.toThrowError(
        NotFoundException,
      );
    });

    it('should return a not found exception', () => {
      const id = mockUuid;

      jest
        .spyOn(citiesRepository, 'delete')
        .mockResolvedValue({ affected: 0 } as DeleteResult);

      expect(citiesService.deleteCity(id)).rejects.toThrowError(
        NotFoundException,
      );
    });
  });
});
