export const BASE_URL =
  process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : 'http://101.43.110.249:8000';
export const ONTOSERVER_BASE_URL = 'https://r4.ontoserver.csiro.au/fhir';
// export const BASE_URL = 'http://di-gateway:8000';

// Auth module
export const EMAIL_LOGIN_URL = '/auth/login/email';
export const LOG_OUT_URL = '/auth/logout';
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
export const MAP_URL = '/center/dashboard/predict';

export const UIL_URL = '/center';
export const UIL_BY_GROUP = '/center/groups';
export const UIL_ALL = '/center/concepts/all';

// Profile module
export const USER_PROFILE_URL = '/auth/user';

// Avatar module
export const AVATAR_URL = '/auth/user/avatar';

// Dashboard module
export const DASHBOARD_INFO_URL = '/center/dashboard';

// CodeSystem module
export const CODE_SYSTEM_URL = '/center/codesystem';
export const CODE_SYSTEM_VERSION_URL = '/center/codesystem/versions';
export const CODE_SYSTEM_GROUP_URL = '/center/codesystem/groups';
export const CODE_SYSTEM_DOWNLOAD = '/center/codesystem/download';

// Register module
export const REGISTER_URL = '/register';
