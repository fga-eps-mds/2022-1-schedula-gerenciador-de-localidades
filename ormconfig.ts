import { DataSource } from 'typeorm';

export const connectionSource = new DataSource({
  type: 'postgres',
  host: 'localhost',
  port: 5104,
  username: 'postgres',
  password: 'postgres',
  database: 'schedula_location',
  synchronize: true,
  entities: ['src/**/*.entity.ts'],
  migrations: ['./migrations/*.ts'],
  subscribers: ['subscriber/*.ts'],
  migrationsTableName: 'TypeOrmMigrations',
});
