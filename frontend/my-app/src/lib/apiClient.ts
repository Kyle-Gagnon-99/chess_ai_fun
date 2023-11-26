import createClient from 'openapi-fetch';
import { paths } from './openapi';

const baseUrl = 'http://localhost:8000';

export const client = createClient<paths>({
    baseUrl: baseUrl,
});

export const { GET, POST, PUT, DELETE } = client;
