import http from '../../utils/http';
import { DASHBOARD_INFO_URL } from '../../utils/constant/url';

export const getDashboardInfo = () => {
  const topLeftInfo = http.get(`${DASHBOARD_INFO_URL}/top-left`);
  const topMiddleInfo = http.get(`${DASHBOARD_INFO_URL}/top-middle`);
  const topRightInfo = http.get(`${DASHBOARD_INFO_URL}/top-right`);

  return Promise.all([topLeftInfo, topMiddleInfo, topRightInfo]);
};

export const getBarChartInfo = () => {
  return http.get(`${DASHBOARD_INFO_URL}/item-status-ratio`);
};

export const getHelloInfo = () => {
  return http.get(`${DASHBOARD_INFO_URL}/hello`);
};
