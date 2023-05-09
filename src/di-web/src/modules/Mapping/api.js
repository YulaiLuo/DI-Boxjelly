import { ONTOSERVER_BASE_URL, MAP_URL, MAP_TASK_URL } from '../../utils/constant/url';
import axios from 'axios';
import http from '../../utils/http';

const instance = axios.create({
  baseURL: ONTOSERVER_BASE_URL,
});

const _mapParametersToRes = (parameters) => {
  const matches = parameters.filter((value) => value.name === 'match');
  const concepts = matches.map((match) => match.part?.filter((value) => value.name === 'concept'));
  if (!concepts.length) return Promise.reject('fail to match');
  const valueCodings = concepts.map((concept) => concept[0]?.valueCoding);
  const disorders = valueCodings.filter(
    (valueCoding) => valueCoding.extension[0]?.valueString === 'disorder'
  );
  if (!disorders.length) return Promise.reject('fail to match');
  const mappedRes = disorders.map((disorder) => ({
    code: disorder.code,
    display: disorder.display.split(' (')[0],
    mappingSuccess: true,
  }));
  // TODO: currently we haven't found a way to select the most appropriate result among multiple possible mappings
  return Promise.resolve(mappedRes[0]);
};

// export const mapSingleText = (code) => http.get(SINGLE_TEXT_MAPPING_URL, { code });
export const mapSingleText = (text) => {
  return http.post(`${MAP_URL}`, {texts:[text]}, {})
}

// export const mapMultipleText = async (codes) => {
//   const entry = codes.map((code) => {
//     return {
//       resource: {
//         resourceType: 'Parameters',
//         parameter: [
//           {
//             name: 'url',
//             valueUri: 'http://ontoserver.csiro.au/fhir/ConceptMap/automapstrategy-MML',
//           },
//           {
//             name: 'coding',
//             valueCoding: {
//               display: code,
//             },
//           },
//           {
//             name: 'target',
//             valueUri: 'http://snomed.info/sct?fhir_vs',
//           },
//           {
//             name: 'system',
//             valueUri: 'http://ontoserver.csiro.au/fhir/CodeSystem/codesystem-terms',
//           },
//         ],
//       },
//       request: {
//         method: 'POST',
//         url: ONTOSERVER_TRANSLATE,
//       },
//     };
//   });

//   return instance
//     .post('', {
//       resourceType: 'Bundle',
//       type: 'batch',
//       entry: entry,
//     })
//     .then((res) => {
//       const entry = res.data?.entry;
//       const parameters = entry.map((value) => value.resource?.parameter);
//       const result = parameters.map((parameter) => _mapParametersToRes(parameter));
//       const settledRes = Promise.allSettled(result).then((values) => {
//         const result = values.map((value) => {
//           if (value.status === 'fulfilled') return value.value;
//           else
//             return {
//               code: null,
//               display: value.reason,
//               mappingSuccess: false,
//             };
//         });
//         return result;
//       });
//       return settledRes;
//     })
//     .catch((e) => {
//       return e;
//     });
// };

// Create a mapping task
export const createMappingTask = (file, teamId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('create_by', '60c879e72cb0e6f96d6b0f65');
  return http.postFormData(MAP_TASK_URL, formData);
};

// Get mapping task detail
export const getMappingTaskDetail = (taskId, page = 1, size = 10) => {
  return http.get(`${MAP_TASK_URL}/${taskId}`, { page, size });
};

// Get mapping task meta detail
export const getMappingTaskMetaDetail = (taskId) => {
  return http.get(`${MAP_TASK_URL}/${taskId}/meta`);
};

export const exportFile = async(taskId) => {
  try {
    const response = await http.get(`${MAP_TASK_URL}/${taskId}/download`, {}, {
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `map_task_export_${new Date().toISOString().slice(0, 10)}_${new Date().toLocaleTimeString('it-IT').replace(/:/g, '')}.csv`);
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  } catch (error) {
    console.error('Error downloading CSV:', error);
  }

}
