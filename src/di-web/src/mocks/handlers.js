import authMockService from './api/auth';
import uilMockService from './api/uil';

export const handlers = [...authMockService, ...uilMockService];
