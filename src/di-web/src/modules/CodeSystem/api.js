import Cookies from 'js-cookie';
import http from '../../utils/http';
import { CODE_SYSTEM_URL, CODE_SYSTEM_VERSION_URL } from '../../utils/constant/url';

export const getCodeSystemList = (version = 'latest') => {
  return http.get(CODE_SYSTEM_URL, { version });
};

export const createNewCodeSystem = (file, name, description, version) => {
  const csrfCookie = Cookies.get('csrf_access_token');
  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', name);
  formData.append('description', description);
  formData.append('version', version);
  return http.postFormData(CODE_SYSTEM_URL, formData, { 'X-CSRF-TOKEN': csrfCookie });
};

export const getAllCodeSystemVersion = () => {
  return http.get(CODE_SYSTEM_VERSION_URL);
};

export const deleteCodeSystem = (version) => {
  return http.deleteData(CODE_SYSTEM_URL, { version });
};
