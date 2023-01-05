import { DataSource } from 'typeorm';

export const connectionSource = new DataSource({
  type: 'postgres',
  host: process.env.DATABASE_HOST,
  port: parseInt(process.env.DATABASE_PORT) || 5104,
  username: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASS,
  database: process.env.DATABASE_DB,
  synchronize: true,
  entities: ['src/**/*.entity.ts'],
  migrations: ['./migrations/*.ts'],
  subscribers: ['subscriber/*.ts'],
  migrationsTableName: 'TypeOrmMigrations',
});
