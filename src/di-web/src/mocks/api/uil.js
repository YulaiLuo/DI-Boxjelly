/**
 * Task mock APIs
 */
import { rest } from 'msw';
import { BASE_URL, MAP_TASK_URL } from '../../utils/constant/url';
import { mapTaskDetail, allMappingTasks } from '../data/taskData';

/**
 * Create a new task
 */
export const createTaskMockService = rest.post(
  `${BASE_URL}${MAP_TASK_URL}`,
  async (req, res, ctx) => {
    return res(
      ctx.json({
        data: {
          id: '52',
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
  `${BASE_URL}${MAP_TASK_URL}/52`,
  async (req, res, ctx) => {
    console.log(req);
    const page = req.url.searchParams.get('page');
    const size = req.url.searchParams.get('size');
    // const id = req.url.searchParams.get('taskId');

    return res(
      ctx.json({
        data: {
          id: '52',
          items: mapTaskDetail,
          page,
          size,
          page_num: 175,
          status: 'success',
        },
        msg: 'success',
        code: 200,
      })
    );
  }
);

/**
 * Get all mapping tasks info with pagination
 */
export const getAllMappingTasks = rest.get(`${BASE_URL}${MAP_TASK_URL}`, async (req, res, ctx) => {
  const page = req.url.searchParams.get('page');
  const size = req.url.searchParams.get('size');

  return res(
    ctx.json({
      data: {
        page: Number(page),
        size: Number(size),
        page_num: 6,
        tasks: allMappingTasks,
      },
      msg: 'success',
      code: 200,
    })
  );
});

const uilMockService = [createTaskMockService, getTaskDetailMockService, getAllMappingTasks];

export default uilMockService;
