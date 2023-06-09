export const BASE_URL =
  process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : process.env.REACT_APP_PROD_BASE_URL;

export const DOMAIN_URL =
  process.env.NODE_ENV === 'development' ? 'http://localhost:3000' : process.env.REACT_APP_PROD_DOMAIN_URL;

// Auth module
export const EMAIL_LOGIN_URL = '/auth/login/email';
export const LOG_OUT_URL = '/auth/logout';
export const TEAM_INFO_URL = '/auth/team';

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
export const CODE_SYSTEM_DOWNLOAD_URL = '/center/codesystem/download';

// Register module
export const REGISTER_URL = '/auth/team/accept';
