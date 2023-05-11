import http from '../../utils/http';
import { UIL_URL } from '../../utils/constant/url';

export const getCodeSystemList = (team_id, code_system_id) => {
  return http.get(`${UIL_URL}`, { team_id, code_system_id });
};
