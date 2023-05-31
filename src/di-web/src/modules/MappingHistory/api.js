import http from '../../utils/http';
import { MAP_BOARDS_URL, MAP_TASK_URL } from '../../utils/constant/url';
import { getCSRFTokenHeader } from '../../utils/auth';

// Get all map tasks with pagination
export const getAllMappingTasks = (team_id, board_id, page, size) => {
  return http.get(`${MAP_BOARDS_URL}/tasks`, { team_id, board_id, page, size });
};

// Get mapping task detail
export const getMappingTaskDetail = (task_id, team_id, board_id, page = 1, size = 10) => {
  return http.get(`${MAP_TASK_URL}/detail`, { task_id, team_id, board_id, page, size });
};

export const deleteMappingTask = (task_id, team_id, board_id) => {
  const headers = getCSRFTokenHeader();
  return http.deleteData(`${MAP_BOARDS_URL}/tasks`, { task_id, team_id, board_id }, headers);
};
