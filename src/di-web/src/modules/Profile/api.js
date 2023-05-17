import http from '../../utils/http';
import { USER_PROFILE_URL } from '../../utils/constant/url';
import { getCSRFTokenHeader } from '../../utils/auth';

// Get user profile details
export const getUserProfile = (user_id) => {
  return http.get(`${USER_PROFILE_URL}?user_id=${user_id}`);
};

// Update user profile
export const updateUserProfile = (user_id, data) => {
  const headers = getCSRFTokenHeader();
  return http.put(`${USER_PROFILE_URL}?user_id=${user_id}`, data, headers);
};
