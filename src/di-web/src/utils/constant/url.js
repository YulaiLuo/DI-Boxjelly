export const BASE_URL =
  process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : 'http://101.43.110.249:8000';
export const ONTOSERVER_BASE_URL = 'https://r4.ontoserver.csiro.au/fhir';
// export const BASE_URL = 'http://di-gateway:8000';

// Auth module
export const EMAIL_LOGIN_URL = '/auth/login/email';
export const TEAM_INFO_URL = '/auth/team';

// Mapping module
export const SINGLE_TEXT_MAPPING_URL = '/map/ontoserver/translate';
export const ONTOSERVER_TRANSLATE = '/ConceptMap/$translate';

// UIL board
export const MAP_BOARDS_URL = '/uil/boards';

// UIL task
export const MAP_TASK_URL = '/uil/boards/task';

// UIL task item
export const MAP_ITEM_URL = '/uil/task';

// MedCAT mapping
export const MAP_URL = '/map/translate';

export const UIL_URL = '/uil';
export const UIL_BY_GROUP = '/uil/groups';
export const UIL_ALL = '/uil/concepts/all';
