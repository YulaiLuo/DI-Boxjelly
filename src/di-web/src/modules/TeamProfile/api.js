import http from '../../utils/http';
import { TEAM_INFO_URL } from '../../utils/constant/url';

export const getTeamInfo = (team_id) => {
  return http.get(`${TEAM_INFO_URL}`, { team_id });
};

export const getInvitationLink = (team_id) => {
  return http.get(`${TEAM_INFO_URL}/invite`, { team_id });
};

export const deleteTeamMember = (team_id, user_id) => {
  return http.deleteData(`${TEAM_INFO_URL}/member`, { team_id, user_id });
};
