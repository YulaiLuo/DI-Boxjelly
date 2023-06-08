// The http utility is imported from the utility folder
import http from '../../utils/http';
// The constant URL for team information is imported from the constants URL file
import { TEAM_INFO_URL } from '../../utils/constant/url';

// Function for fetching team information from the server
// It sends a GET request to the TEAM_INFO_URL endpoint
// The team_id is sent as a parameter to the request
export const getTeamInfo = (team_id) => {
  return http.get(`${TEAM_INFO_URL}`, { team_id });
};

// Function for generating an invitation link for a given team
// It sends a GET request to the TEAM_INFO_URL/invite endpoint
// The team_id is sent as a parameter to the request
export const getInvitationLink = (team_id) => {
  return http.get(`${TEAM_INFO_URL}/invite`, { team_id });
};

// Function for deleting a team member from the server
// It sends a DELETE request to the TEAM_INFO_URL/member endpoint
// The team_id and user_id are sent as parameters to the request
export const deleteTeamMember = (team_id, user_id) => {
  return http.deleteData(`${TEAM_INFO_URL}/member`, { team_id, user_id });
};
