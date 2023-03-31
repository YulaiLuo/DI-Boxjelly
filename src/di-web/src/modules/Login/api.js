import http from '../../utils/http';
import { EMAIL_LOGIN_URL } from '../../constant/url';

export const login = (data) => http.post(EMAIL_LOGIN_URL, data);
