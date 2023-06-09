// Importing required modules
import http from '../../utils/http';
import { DASHBOARD_INFO_URL } from '../../utils/constant/url';

// Fetches the information to be displayed on the dashboard.
// There are three requests sent concurrently, and this function
// Returns a Promise that resolves when all three have returned.
export const getDashboardInfo = () => {
  const topLeftInfo = http.get(`${DASHBOARD_INFO_URL}/top-left`);
  const topMiddleInfo = http.get(`${DASHBOARD_INFO_URL}/top-middle`);
  const topRightInfo = http.get(`${DASHBOARD_INFO_URL}/top-right`);

  return Promise.all([topLeftInfo, topMiddleInfo, topRightInfo]);
};

// Fetches the information required for the Bar Chart.
export const getBarChartInfo = () => {
  return http.get(`${DASHBOARD_INFO_URL}/item-status-ratio`);
};

// Fetches the "Hello" information to be displayed on the dashboard.
export const getHelloInfo = () => {
  return http.get(`${DASHBOARD_INFO_URL}/hello`);
};
