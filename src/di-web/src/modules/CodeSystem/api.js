import http from '../../utils/http';
import { UIL_URL, UIL_BY_GROUP } from '../../utils/constant/url';

export const getCodeSystemList = (team_id, code_system_id) => {
  return http.get(`${UIL_URL}`, { team_id, code_system_id });
};

export const getCodeSystemListByGroup = (group_id) => {
  return http.get(`${UIL_BY_GROUP}`, { group_id });
};
