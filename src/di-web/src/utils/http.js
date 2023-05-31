import axios from 'axios';
import { message } from 'antd';
import { BASE_URL } from './constant/url';
import { getCSRFTokenHeader } from './auth';
import { redirectToLogin } from './router';

const instance = axios.create({
  baseURL: BASE_URL,
  timeout: 8000,
  withCredentials: true,
});

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
    const errMsg = error.response.data?.err;
    if (
      error.response.data?.code === 401 &&
      (errMsg === 'TOKEN_EXPIRED' || errMsg === 'UNAUTHORIZED')
    ) {
      if (errMsg === 'TOKEN_EXPIRED') message.error('Token has expired!');
      else message.error('Unauthorized access!');
      redirectToLogin();
      return;
    }
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

const post = (api, data, headers = getCSRFTokenHeader()) => {
  headers['Content-Type'] = 'application/json;charset=utf-8';
  return _post(api, JSON.stringify(data), headers);
};

const postFormData = (api, data, headers = {}) => {
  headers['Content-Type'] = 'multipart/form-data';
  return _post(api, data, headers);
};

const deleteData = (api, params = {}, headers = getCSRFTokenHeader()) => {
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

const put = (api, data, headers = getCSRFTokenHeader()) => {
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
