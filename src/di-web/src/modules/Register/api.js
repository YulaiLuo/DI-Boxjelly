import http from '../../utils/http';
import { REGISTER_URL } from '../../utils/constant/url';
import { getCSRFTokenHeader } from '../../utils/auth';

export const registerUser = (data) => {
    const headers = getCSRFTokenHeader();
    return http.postFormData(`${REGISTER_URL}`, data, headers);
};
