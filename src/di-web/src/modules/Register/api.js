import http from '../../utils/http';
import { REGISTER_URL } from '../../utils/constant/url';

export const registerUser = (data) => {
    return http.postFormData(`${REGISTER_URL}`, data);
};
