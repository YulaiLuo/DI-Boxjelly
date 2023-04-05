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

// export const checkAuthentication = () => {
//   const hasAccessToken = !!Cookies.get(AUTH.ACCESS_TOKEN_COOKIE);
//   const hasRefreshToken = !!Cookies.get(AUTH.REFRESH_TOKEN_COOKIE);
//   return hasAccessToken || hasRefreshToken;
// };
