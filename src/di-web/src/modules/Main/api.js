// This module defines the HTTP API calls that are used in the Main module of the application.
// It utilizes a http utility and axios for making these calls to server endpoints.
// It has functions for getting, editing, creating and deleting boards, and for logging out.
import http from '../../utils/http';
import { MAP_BOARDS_URL, LOG_OUT_URL } from '../../utils/constant/url';

// Function to get the list of boards for a given team
export const getBoardList = (team_id) => {
  return http.get(MAP_BOARDS_URL, { team_id });
};

// Function to edit a specific board identified by its id
export const editBoard = (board_id, team_id, new_name, new_description) => {
  return http.put(MAP_BOARDS_URL, { board_id, team_id, new_name, new_description });
};

// Function to create a new board for a team
export const createBoard = (team_id, name, description) => {
  return http.post(MAP_BOARDS_URL, { team_id, name, description });
};

// Function to delete a specific board
export const deleteBoard = (board_id, team_id) => {
  return http.deleteData(MAP_BOARDS_URL, { board_id, team_id });
};

// Function to logout a user
export const logout = () => {
  return http.post(LOG_OUT_URL);
};
