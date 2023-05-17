import http from '../../utils/http';
import { MAP_BOARDS_URL } from '../../utils/constant/url';

export const getBoardList = (team_id) => {
  return http.get(`${MAP_BOARDS_URL}`, { team_id });
};

export const editBoard = (board_id, team_id, new_name, new_description) => {
  return http.put(`${MAP_BOARDS_URL}`, { board_id, team_id, new_name, new_description });
};

export const createBoard = (team_id, name, description) => {
  return http.post(`${MAP_BOARDS_URL}`, { team_id, name, description });
};

export const deleteBoard = (board_id, team_id) => {
  return http.deleteData(`${MAP_BOARDS_URL}`, { board_id, team_id });
};
