/**
 * Task mock APIs
 */
import { rest } from 'msw';
import {
  BASE_URL,
  MAP_TASK_URL,
  UIL_URL,
  MAP_BOARD_URL,
  UIL_BY_GROUP,
} from '../../utils/constant/url';
import { mapTaskDetail, allMappingTasks, codeSystemGroups } from '../data/taskData';

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
  `${BASE_URL}${MAP_TASK_URL}`,
  async (req, res, ctx) => {
    console.log(req);
    const page = req.url.searchParams.get('page');
    const size = req.url.searchParams.get('size');
    const taskId = req.url.searchParams.get('task_id');
    // const id = req.url.searchParams.get('taskId');

    return res(
      ctx.json({
        data: {
          id: taskId,
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
export const getAllMappingTasks = rest.get(`${BASE_URL}${MAP_BOARD_URL}`, async (req, res, ctx) => {
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

export const getCodeSystemList = rest.get(`${BASE_URL}${UIL_URL}`, async (req, res, ctx) => {
  const team_id = req.url.searchParams.get('team_id');
  const code_system_id = req.url.searchParams.get('code_system_id');

  return res(
    ctx.json({
      data: {
        code_system_id: '3423423423423423',
        create_at: 'Tue, 09 May 2023 13:49:29 GMT',
        description: 'some des',
        groups: codeSystemGroups,
      },
      msg: 'success',
      code: 200,
    })
  );
});

export const getCodeSystemListByGroup = rest.get(
  `${BASE_URL}${UIL_BY_GROUP}`,
  async (req, res, ctx) => {
    console.log('sfsfsf');
    const groupId = req.url.searchParams.get('group_id');
    let data;
    if (groupId === '1') data = codeSystemGroups[0];
    else if (groupId === '2') data = codeSystemGroups[1];
    else data = codeSystemGroups[2];

    return res(
      ctx.json({
        data,
        msg: 'success',
        code: 200,
      })
    );
  }
);

const uilMockService = [
  createTaskMockService,
  getTaskDetailMockService,
  getAllMappingTasks,
  getCodeSystemList,
  getCodeSystemListByGroup,
];

export default uilMockService;
