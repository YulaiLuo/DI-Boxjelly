/**
 * Task mock APIs
 */
import { rest } from 'msw';
import { BASE_URL, MAP_TASK_URL } from '../../utils/constant/url';
import { mapTaskDetail } from '../data/taskData';

/**
 * Create a new task
 */
export const createTaskMockService = rest.post(
  `${BASE_URL}${MAP_TASK_URL}`,
  async (req, res, ctx) => {
    return res(
      ctx.json({
        data: {
          id: '123456',
          num: 1,
          status: 'pending',
        },
        msg: 'success',
        code: 200,
      })
    );
  }
);

/**
 * Get task detail
 */
export const getTaskDetailMockService = rest.get(
  `${BASE_URL}${MAP_TASK_URL}/123456`,
  async (req, res, ctx) => {
    return res(
      ctx.json({
        data: mapTaskDetail,
        msg: 'success',
        code: 200,
      })
    );
  }
);

const uilMockService = [createTaskMockService, getTaskDetailMockService];

export default uilMockService;
