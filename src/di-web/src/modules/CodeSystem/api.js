// Importing required dependencies and constants
import Cookies from 'js-cookie';
import http from '../../utils/http';
import {
  CODE_SYSTEM_URL,
  CODE_SYSTEM_VERSION_URL,
  CODE_SYSTEM_DOWNLOAD_URL,
} from '../../utils/constant/url';

// Function to fetch the list of code systems. The version argument is optional and defaults to 'latest'.
export const getCodeSystemList = (version = 'latest') => {
  return http.get(CODE_SYSTEM_URL, { version });
};

// Function to create a new code system. The CSRF token is fetched from the cookie and added to the request headers for protection against CSRF attacks. 
// The function arguments are appended to form data, which is sent in the POST request.
export const createNewCodeSystem = (file, name, description, version) => {
  const csrfCookie = Cookies.get('csrf_access_token');
  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', name);
  formData.append('description', description);
  formData.append('version', version);
  return http.postFormData(CODE_SYSTEM_URL, formData, { 'X-CSRF-TOKEN': csrfCookie });
};

// Function to fetch all versions of the code systems
export const getAllCodeSystemVersion = () => {
  return http.get(CODE_SYSTEM_VERSION_URL);
};

// Function to delete a code system. The version of the code system to be deleted is passed as an argument.
export const deleteCodeSystem = (version) => {
  return http.deleteData(CODE_SYSTEM_URL, { version });
};

// Function to export a code system. The version of the code system to be exported is passed as an argument. The exported file is downloaded as a blob.
export const exportCodeSystem = async (version) => {
  try {
    const response = await http.get(
      `${CODE_SYSTEM_DOWNLOAD_URL}/${version}`,
      {},
      {
        responseType: 'blob',
      }
    );

    // After the successful response, a URL is created for the blob and a download link is triggered to start the file download.
    const url = window.URL.createObjectURL(new Blob([response]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute(
      'download',
      `code_system_export_${new Date().toISOString().slice(0, 10)}_${new Date()
        .toLocaleTimeString('it-IT')
        .replace(/:/g, '')}.xlsx`
    );
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  } catch (error) {
    // Any errors during the download process are logged to the console
    console.error('Error downloading XLSX:', error);
  }
};
