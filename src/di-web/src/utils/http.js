import axios from 'axios';
import { message } from 'antd';
import { BASE_URL } from './constant/url';

const instance = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 8000,
  withCredentials: true,
});

instance.interceptors.response.use(
  (res) => {
    const { msg } = res.data;
    if (res.status !== 200) {
      message.error(msg);
      throw msg;
    }
    return res.data;
  },
  (error) => {
    const msg = error.response.data?.msg ?? 'something wrong with the network request';
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

const post = (api, data, headers = {}) => {
  headers['Content-Type'] = 'application/json;charset=utf-8';
  return _post(api, JSON.stringify(data), headers);
};

const postFormData = (api, data, headers = {}) => {
  headers['Content-Type'] = 'multipart/form-data';
  return _post(api, data, headers);
};
// eslint-disable-next-line
export default { get, post, postFormData };
