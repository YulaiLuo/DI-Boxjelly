import http from '../../utils/http';
import { MAP_BOARD_URL, MAP_TASK_URL } from '../../utils/constant/url';

// Get all map tasks with pagination
export const getAllMappingTasks = (team_id, board_id, page, size) => {
  return http.get(MAP_BOARD_URL, { team_id, board_id, page, size });
};

// Get mapping task detail
export const getMappingTaskDetail = (taskId, team_id, board_id, page = 1, size = 10) => {
  return http.get(`${MAP_TASK_URL}`, { taskId, team_id, board_id, page, size });
};
