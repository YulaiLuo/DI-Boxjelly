import http from '../../utils/http';
import { MAP_BOARDS_URL } from '../../utils/constant/url';

export const getBoardList = (team_id) => {
  return http.get(`${MAP_BOARDS_URL}`, { team_id });
};
