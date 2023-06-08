// Import necessary modules and constants
import http from '../../utils/http';
import { USER_PROFILE_URL } from '../../utils/constant/url';
import { getCSRFTokenHeader } from '../../utils/auth';

// Function to get user profile details from the server using a GET request
// user_id is passed as a parameter to identify the user whose data is to be fetched
export const getUserProfile = (user_id) => {
  return http.get(`${USER_PROFILE_URL}?user_id=${user_id}`);
};

// Function to update user profile details on the server using a PUT request
// user_id and data (new profile details) are passed as parameters
// CSRF token is fetched and included in the request headers for security
export const updateUserProfile = (user_id, data) => {
  const headers = getCSRFTokenHeader();
  return http.put(`${USER_PROFILE_URL}?user_id=${user_id}`, data, headers);
};
