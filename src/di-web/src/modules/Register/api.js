// Import necessary modules and variables
import http from '../../utils/http';
import { REGISTER_URL } from '../../utils/constant/url';

// Function to send a POST request to the register endpoint with the provided data
export const registerUser = (data) => {
    return http.postFormData(`${REGISTER_URL}`, data);
};
