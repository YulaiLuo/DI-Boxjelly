import http from '../../utils/http';
import { MAP_BOARDS_URL, MAP_TASK_URL } from '../../utils/constant/url';
import { getCSRFTokenHeader } from '../../utils/auth';

// The getAllMappingTasks function sends a GET request to fetch all the mapping tasks
// associated with a particular team and board. The response is paginated according to the
// 'page' and 'size' parameters.
export const getAllMappingTasks = (team_id, board_id, page, size) => {
  return http.get(`${MAP_BOARDS_URL}/tasks`, { team_id, board_id, page, size });
};

// The getMappingTaskDetail function sends a GET request to fetch the detailed information
// of a specific mapping task identified by the 'task_id', 'team_id', and 'board_id' parameters.
// The response is paginated according to the 'page' and 'size' parameters.
export const getMappingTaskDetail = (task_id, team_id, board_id, page = 1, size = 10) => {
  return http.get(`${MAP_TASK_URL}/detail`, { task_id, team_id, board_id, page, size });
};

// The deleteMappingTask function sends a DELETE request to remove a specific mapping task
// identified by the 'task_id', 'team_id', and 'board_id' parameters.
// This function first gets a CSRF token to be included in the request header for security.
export const deleteMappingTask = (task_id, team_id, board_id) => {
  const headers = getCSRFTokenHeader();
  return http.deleteData(`${MAP_BOARDS_URL}/tasks`, { task_id, team_id, board_id }, headers);
};
