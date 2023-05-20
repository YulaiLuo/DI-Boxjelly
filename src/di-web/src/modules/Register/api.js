import http from '../../utils/http';
import { REGISTER_URL } from '../../utils/constant/url';
// import { getCSRFTokenHeader } from '../../utils/auth';

export const registerUser = (data) => {
    const headers = { 'Content-Type': 'application/json' };
    // const headers = getCSRFTokenHeader();
    return http.post(`${REGISTER_URL}`, data, headers);
};
  