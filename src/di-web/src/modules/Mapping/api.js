import Cookies from 'js-cookie';
import {
  // ONTOSERVER_BASE_URL,
  MAP_URL,
  // MAP_TASK_URL,
  MAP_BOARDS_URL,
  MAP_TASK_META_URL,
  MAP_TASK_DETAIL_URL,
  MAP_TASK_DOWNLOAD_URL,
  MAP_TASK_CURATE_URL,
} from '../../utils/constant/url';
import http from '../../utils/http';

// export const mapSingleText = (code) => http.get(SINGLE_TEXT_MAPPING_URL, { code });
export const mapSingleText = (text) => {
  const csrfCookie = Cookies.get('csrf_access_token');
  return http.post(`${MAP_URL}`, { text: text }, { 'X-CSRF-TOKEN': csrfCookie });
};

// Create a mapping task
export const createMappingTask = (teamId, boardId, file) => {
  const csrfCookie = Cookies.get('csrf_access_token');
  const formData = new FormData();
  formData.append('file', file);
  formData.append('team_id', teamId);
  formData.append('board_id', boardId);
  return http.postFormData(`${MAP_BOARDS_URL}/tasks`, formData, { 'X-CSRF-TOKEN': csrfCookie });
};

// Get mapping task detail
export const getMappingTaskDetail = (
  task_id,
  team_id,
  board_id,
  page = 1,
  size = 10,
  filter = {}
) => {
  let params = {
    task_id,
    team_id,
    board_id,
    page,
    size,
  };
  if (filter.mappingStatus) {
    params = {
      ...params,
      status: filter.mappingStatus,
    };
  }
  if (filter.source) {
    params = {
      ...params,
      ontology: filter.source,
    };
  }
  if (
    filter.minConfidence !== 'undefined' &&
    filter.maxConfidence !== 'undefined' &&
    filter.minConfidence <= filter.maxConfidence
  ) {
    params = {
      ...params,
      min_accuracy: filter.minConfidence,
      max_accuracy: filter.maxConfidence,
    };
  }
  if (filter.mappingStatus === 'fail') {
    delete params.min_accuracy;
    delete params.max_accuracy;
  }
  return http.get(`${MAP_TASK_DETAIL_URL}`, params);
};

// Get mapping task meta detail
export const getMappingTaskMetaDetail = (task_id) => {
  return http.get(`${MAP_TASK_META_URL}`, { task_id });
};

export const exportFile = async (team_id, task_id) => {
  try {
    const response = await http.get(
      `${MAP_TASK_DOWNLOAD_URL}`,
      { team_id, task_id },
      {
        responseType: 'blob',
      }
    );

    const url = window.URL.createObjectURL(new Blob([response]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute(
      'download',
      `map_task_export_${new Date().toISOString().slice(0, 10)}_${new Date()
        .toLocaleTimeString('it-IT')
        .replace(/:/g, '')}.csv`
    );
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  } catch (error) {
    console.error('Error downloading CSV:', error);
  }
};

export const curateMapping = (map_item_id, concept_name, code_system_version) => {
  return http.post(MAP_TASK_CURATE_URL, { map_item_id, concept_name, code_system_version });
};
