import { createBrowserHistory } from 'history';

const history = createBrowserHistory();

export function redirectToLogin() {
  console.log('first', history);
  history.push('/login');
  window.location.hash = '/login';
  window.location.hash = '';
}

export default history;
