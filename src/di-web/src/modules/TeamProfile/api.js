import http from '../../utils/http';
import { TEAM_INFO_URL } from '../../utils/constant/url';

export const getTeamInfo = (team_id) => {
  return http.get(`${TEAM_INFO_URL}`, { team_id });
};
