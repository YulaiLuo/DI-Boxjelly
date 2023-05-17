import axios from 'axios';
import { message } from 'antd';
import { BASE_URL } from './constant/url';
import { getCSRFTokenHeader } from './auth';

const instance = axios.create({
  // baseURL: 'http://localhost:8000',
  baseURL: BASE_URL,
  timeout: 8000,
  withCredentials: true,
});

const csrfTokenHeader = getCSRFTokenHeader();

instance.interceptors.response.use(
  (res) => {
    const { msg } = res.data;
    if (res.status >= 300) {
      message.error(msg);
      throw msg;
    }
    return res.data;
  },
  (error) => {
    const msg = error.response.data?.msg ?? 'Something wrong with the network request';
    message.error(msg);
    throw error;
  }
);

const get = (api, params = {}, headers = {}) => {
  return new Promise((resolve, reject) => {
    instance
      .get(api, { params, headers })
      .then((res) => {
        resolve(res);
      })
      .catch((error) => {
        reject(error);
      });
  });
};

const _post = (api, data, headers = {}) => {
  return new Promise((resolve, reject) => {
    instance
      .post(api, data, { headers })
      .then((res) => {
        resolve(res);
      })
      .catch((error) => {
        reject(error);
      });
  });
};

const post = (api, data, headers = csrfTokenHeader) => {
  headers['Content-Type'] = 'application/json;charset=utf-8';
  return _post(api, JSON.stringify(data), headers);
};

const postFormData = (api, data, headers = {}) => {
  headers['Content-Type'] = 'multipart/form-data';
  return _post(api, data, headers);
};

const deleteData = (api, params = {}, headers = csrfTokenHeader) => {
  return new Promise((resolve, reject) => {
    instance
      .delete(api, { params, headers })
      .then((res) => {
        resolve(res);
      })
      .catch((error) => {
        reject(error);
      });
  });
};

const put = (api, data, headers = csrfTokenHeader) => {
  return new Promise((resolve, reject) => {
    instance
      .put(api, data, { headers })
      .then((res) => {
        resolve(res);
      })
      .catch((error) => {
        reject(error);
      });
  });
};

// eslint-disable-next-line
export default { get, post, postFormData, deleteData, put };
