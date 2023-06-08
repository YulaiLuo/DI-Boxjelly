// This module defines the HTTP API calls that are used in the Mapping module of the application.
// It utilizes a http utility and axios for making these calls to server endpoints.
// It provides functions to map a single text, create a mapping task, get mapping task detail,
// get mapping task meta detail, export file and curate mapping.
import Cookies from 'js-cookie';
import {
  MAP_URL,
  MAP_BOARDS_URL,
  MAP_TASK_META_URL,
  MAP_TASK_DETAIL_URL,
  MAP_TASK_DOWNLOAD_URL,
  MAP_TASK_CURATE_URL,
} from '../../utils/constant/url';
import http from '../../utils/http';

// Function to map a single text
export const mapSingleText = (text) => {
  const csrfCookie = Cookies.get('csrf_access_token');
  return http.post(`${MAP_URL}`, { text: text }, { 'X-CSRF-TOKEN': csrfCookie });
};

// Function to create a new mapping task
export const createMappingTask = (teamId, boardId, file) => {
  const csrfCookie = Cookies.get('csrf_access_token');
  const formData = new FormData();
  formData.append('file', file);
  formData.append('team_id', teamId);
  formData.append('board_id', boardId);
  return http.postFormData(`${MAP_BOARDS_URL}/tasks`, formData, { 'X-CSRF-TOKEN': csrfCookie });
};

// Function to get detailed information of a mapping task
export const getMappingTaskDetail = (
  task_id,
  team_id,
  board_id,
  page = 1,
  size = 10,
  filter = {}
) => {
  // Additional logic to handle filtering parameters for the mapping task details
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

// Function to get meta detail of a mapping task
export const getMappingTaskMetaDetail = (task_id) => {
  return http.get(`${MAP_TASK_META_URL}`, { task_id });
};

// Function to export a mapping task as a CSV file
export const exportFile = async (team_id, task_id) => {
  // Logic to handle download of CSV file
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
    // Error handling for download failures
    console.error('Error downloading CSV:', error);
  }
};

// Function to curate a mapping
export const curateMapping = (map_item_id, concept_name, code_system_version) => {
  return http.post(MAP_TASK_CURATE_URL, { map_item_id, concept_name, code_system_version });
};
