import Cookies from 'js-cookie';
import http from '../../utils/http';
import {
  CODE_SYSTEM_URL,
  CODE_SYSTEM_VERSION_URL,
  CODE_SYSTEM_DOWNLOAD_URL,
} from '../../utils/constant/url';

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

export const exportCodeSystem = async (version) => {
  try {
    const response = await http.get(
      `${CODE_SYSTEM_DOWNLOAD_URL}/${version}`,
      {},
      {
        responseType: 'blob',
      }
    );

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
    console.error('Error downloading XLSX:', error);
  }
};
