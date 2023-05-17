import Cookies from 'js-cookie';
import { AUTH } from './constant/constants';

// export const setTokens = () => {
//   const cookiePairs = document.cookie.split('; ');
//   for (const pair of cookiePairs) {
//     const [key, value] = pair.split('=');
//     if (key === AUTH.ACCESS_TOKEN_COOKIE || key === AUTH.REFRESH_TOKEN_COOKIE) {
//       Cookies.set(key, value);
//     }
//   }
// };

// export const removeTokens = () => {
//   Cookies.remove(AUTH.ACCESS_TOKEN_COOKIE);
//   Cookies.remove(AUTH.REFRESH_TOKEN_COOKIE);
// }

export const checkAuthentication = () => {
  const hasCsrfAccessCookie = !!Cookies.get(AUTH.CSRF_ACCESS_TOKEN_COOKIE);
  const hasCsrfRefreshCookie = !!Cookies.get(AUTH.CSRF_REFRESH_TOKEN_COOKIE);
  localStorage.setItem('csrf_access_token', Cookies.get(AUTH.CSRF_ACCESS_TOKEN_COOKIE));
  localStorage.setItem('csrf_refresh_token', Cookies.get(AUTH.CSRF_REFRESH_TOKEN_COOKIE));
  return hasCsrfAccessCookie || hasCsrfRefreshCookie;
};

export const getCSRFTokenHeader = () => {
  const csrfCookie = Cookies.get(AUTH.CSRF_ACCESS_TOKEN_COOKIE);
  return { 'X-CSRF-TOKEN': csrfCookie };
};
