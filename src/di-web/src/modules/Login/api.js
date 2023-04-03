import http from '../../utils/http';
import { EMAIL_LOGIN_URL } from '../../utils/constant/url';

export const login = (data) => http.postFormData(EMAIL_LOGIN_URL, data, {'Access-Control-Allow-Origin': '*',});
