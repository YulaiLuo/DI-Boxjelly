import Cookies from 'js-cookie';
import { AUTH } from './constant/constants';

export const checkAuthentication = () => {
  const hasCsrfAccessCookie = !!Cookies.get(AUTH.CSRF_ACCESS_TOKEN_COOKIE);
  const hasCsrfRefreshCookie = !!Cookies.get(AUTH.CSRF_REFRESH_TOKEN_COOKIE);

  return hasCsrfAccessCookie || hasCsrfRefreshCookie;
};

export const getCSRFTokenHeader = () => {
  const csrfCookie = Cookies.get(AUTH.CSRF_ACCESS_TOKEN_COOKIE);
  return { 'X-CSRF-TOKEN': csrfCookie };
};
