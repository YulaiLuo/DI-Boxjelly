import http from '../../utils/http';
import { MAP_BOARD_URL, MAP_TASK_URL } from '../../utils/constant/url';

// Get all map tasks with pagination
export const getAllMappingTasks = (team_id, board_id, page, size) => {
  return http.get(`${MAP_BOARD_URL}`, { team_id, board_id, page, size });
};

// Get mapping task detail
export const getMappingTaskDetail = (task_id, team_id, board_id, page = 1, size = 10) => {
  return http.get(`${MAP_TASK_URL}`, { task_id, team_id, board_id, page, size });
};

export const deleteMappingTask = (task_id, team_id, board_id) => {
  return http.deleteData(`${MAP_TASK_URL}`, { task_id, team_id, board_id });
};
