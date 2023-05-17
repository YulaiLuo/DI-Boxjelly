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
export const MAP_BOARDS_URL = '/center/boards';

// UIL task
export const MAP_TASK_URL = '/center/boards/tasks';
export const MAP_TASK_META_URL = '/center/boards/task/meta';
export const MAP_TASK_DETAIL_URL = '/center/boards/task/detail';
export const MAP_TASK_DOWNLOAD_URL = '/center/boards/task/download';
export const MAP_TASK_CURATE_URL = 'center/boards/task/curate';

// MedCAT mapping
export const MAP_URL = '/map/translate';

export const UIL_URL = '/center';
export const UIL_BY_GROUP = '/center/groups';
export const UIL_ALL = '/center/concepts/all';

// Profile module
export const USER_PROFILE_URL = '/auth/user';
