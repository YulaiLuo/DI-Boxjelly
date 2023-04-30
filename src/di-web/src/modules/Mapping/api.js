// import http from '../../utils/http';
// import { SINGLE_TEXT_MAPPING_URL } from '../../utils/constant/url';
import { ONTOSERVER_BASE_URL, ONTOSERVER_TRANSLATE } from '../../utils/constant/url';
import axios from 'axios';

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
export const mapSingleText = (code) =>
  instance
    .get(ONTOSERVER_TRANSLATE, {
      params: {
        url: 'http://ontoserver.csiro.au/fhir/ConceptMap/automapstrategy-seq;automapstrategy-strict;automapstrategy-MML;automapstrategy-default',
        system: 'http://ontoserver.csiro.au/fhir/CodeSystem/codesystem-terms',
        code,
        target: 'http://snomed.info/sct?fhir_vs',
      },
    })
    .then((res) => {
      const results = res.data?.parameter;
      return _mapParametersToRes(results);
    })
    .catch((e) => {
      return {
        code: null,
        display: e,
        mappingSuccess: false,
      };
    });

export const mapMultipleText = (codes) => {
  const entry = codes.map((code) => {
    return {
      resource: {
        resourceType: 'Parameters',
        parameter: [
          {
            name: 'url',
            valueUri: 'http://ontoserver.csiro.au/fhir/ConceptMap/automapstrategy-MML',
          },
          {
            name: 'coding',
            valueCoding: {
              display: code,
            },
          },
          {
            name: 'target',
            valueUri: 'http://snomed.info/sct?fhir_vs',
          },
          {
            name: 'system',
            valueUri: 'http://ontoserver.csiro.au/fhir/CodeSystem/codesystem-terms',
          },
        ],
      },
      request: {
        method: 'POST',
        url: ONTOSERVER_TRANSLATE,
      },
    };
  });

  return instance
    .post('', {
      resourceType: 'Bundle',
      type: 'batch',
      entry: entry,
    })
    .then((res) => {
      const entry = res.data?.entry;
      const parameters = entry.map((value) => value.resource?.parameter);
      const result = parameters.map((parameter) => _mapParametersToRes(parameter));
      const settledRes = Promise.allSettled(result).then((values) => {
        const result = values.map((value) => {
          if (value.status === 'fulfilled') return value.value;
          else
            return {
              code: null,
              display: value.reason,
              mappingSuccess: false,
            };
        });
        return result;
      });
      return settledRes;
    })
    .catch((e) => {
      return e;
    });
};
