// This file defines the API function required for user login.
// It uses the 'http' utility which is a wrapper for the 'axios' library,
// allowing for easy HTTP requests within the application.
// The 'EMAIL_LOGIN_URL' constant is imported from the utility constants file, which contains all the API endpoint URLs.

// Importing required modules
import http from '../../utils/http';
import { EMAIL_LOGIN_URL } from '../../utils/constant/url';

// The 'login' function makes a POST request to the server for logging in the user.
// It takes in the user's login data (email and password) as an argument.
// The request is made to the 'EMAIL_LOGIN_URL' endpoint with the user data as form data.
export const login = (data) => http.postFormData(EMAIL_LOGIN_URL, data);
