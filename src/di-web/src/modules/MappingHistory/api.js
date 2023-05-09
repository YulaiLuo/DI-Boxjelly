import http from '../../utils/http';
import { MAP_TASK_URL } from '../../utils/constant/url';

// Get all map tasks with pagination
export const getAllMappingTasks = (page, size) => {
  return http.get(MAP_TASK_URL, { page, size });
};

// Get mapping task detail
export const getMappingTaskDetail = (taskId, page = 1, size = 10) => {
  return http.get(`${MAP_TASK_URL}/${taskId}`, { page, size });
};
