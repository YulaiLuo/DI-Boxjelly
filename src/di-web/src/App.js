import { message } from 'antd';
import { useMessageStore } from './store';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import {
  Login,
  Mapping,
  TeamProfile,
  MappingHistory,
  RetrainHistory,
  Main,
  MappingResult,
  Dashboard,
  CodeSystem,
  Profile,
  Register,
} from './modules';
import { checkAuthentication } from './utils/auth';
import history from './utils/router';

function App() {
  // global message display
  const [messageApi, contextHolder] = message.useMessage();

  const loggedIn = checkAuthentication();
  const setMsgApi = useMessageStore((state) => state.setMsgApi);

  setMsgApi(messageApi);

  return (
    <>
      {contextHolder}
      <Router history={history}>
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route element={loggedIn ? <Main /> : <Navigate to="/login" replace />}>
            <Route
              path="/"
              element={
                loggedIn ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />
              }
            />
            <Route
              path="/dashboard"
              element={loggedIn ? <Dashboard /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/mapping-result"
              element={loggedIn ? <MappingResult /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/mapping-history/:id"
              element={loggedIn ? <MappingHistory /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/team-profile"
              element={loggedIn ? <TeamProfile /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/code-system"
              element={loggedIn ? <CodeSystem /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/profile"
              element={loggedIn ? <Profile /> : <Navigate to="/login" replace />}
            />
          </Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
