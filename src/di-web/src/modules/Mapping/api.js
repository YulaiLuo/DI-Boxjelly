// import http from '../../utils/http';
// import { SINGLE_TEXT_MAPPING_URL } from '../../utils/constant/url';
import axios from 'axios';

// export const mapSingleText = (code) => http.get(SINGLE_TEXT_MAPPING_URL, { code });
export const mapSingleText = (code) =>
  axios
    .get('https://r4.ontoserver.csiro.au/fhir/ConceptMap/$translate', {
      params: {
        url: 'http://ontoserver.csiro.au/fhir/ConceptMap/automapstrategy-MML',
        system: 'http://ontoserver.csiro.au/fhir/CodeSystem/codesystem-terms',
        code,
        target: 'http://snomed.info/sct?fhir_vs',
      },
    })
    .then((res) => {
      const results = res.data?.parameter;
      const matches = results.filter((value) => value.name === 'match');
      const concepts = matches.map((match) =>
        match.part?.filter((value) => value.name === 'concept')
      );
      if (!concepts.length) return Promise.reject('fail to match');
      const valueCodings = concepts.map((concept) => concept[0]?.valueCoding);
      const disorders = valueCodings.filter(
        (valueCoding) => valueCoding.extension[0]?.valueString === 'disorder'
      );
      if (!disorders.length) return Promise.reject('fail to match');
      console.log(valueCodings);
      const mappedRes = disorders.map((disorder) => ({
        code: disorder.code,
        display: disorder.display.split(' (')[0],
      }));
      console.log(mappedRes[0])
      // TODO: currently we haven't found a way to select the most appropriate result among multiple possible mappings
      return mappedRes[0];
    })
    .catch((e) => {
      return {
        code: null,
        display: e,
      };
    });
