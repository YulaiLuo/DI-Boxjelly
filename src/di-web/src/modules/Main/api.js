import http from '../../utils/http';
import { MAP_BOARDS } from '../../utils/constant/url';

export const getBoardList = (team_id) => {
  return http.get(`${MAP_BOARDS}`, { team_id });
};
