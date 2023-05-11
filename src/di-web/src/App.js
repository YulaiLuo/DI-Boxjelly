import { message } from 'antd';
import { useMessageStore } from './store';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import {
  Login,
  Mapping,
  Profile,
  MappingHistory,
  RetrainHistory,
  Main,
  MappingResult,
  Dashboard,
  CodeSystem,
} from './modules';
import { checkAuthentication } from './utils/auth';

function App() {
  // global message display
  const [messageApi, contextHolder] = message.useMessage();

  const loggedIn = process.env.NODE_ENV === 'development' || checkAuthentication();
  const setMsgApi = useMessageStore((state) => state.setMsgApi);

  setMsgApi(messageApi);
  // document.cookie = "cookieName=cookieValue; SameSite=None; Secure";
  // const loggedIn = checkAuthentication();

  return (
    <>
      {contextHolder}
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          {/* <Route path="/" element={<Navigate to="dashboard/mapping"/>} /> */}
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
              path="/mapping"
              element={loggedIn ? <Mapping /> : <Navigate to="/login" replace />}
            />

            <Route
              path="/mapping-result"
              element={loggedIn ? <MappingResult /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/mapping-history"
              element={loggedIn ? <MappingHistory /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/retrain-history"
              element={loggedIn ? <RetrainHistory /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/profile"
              element={loggedIn ? <Profile /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/code-system"
              element={loggedIn ? <CodeSystem /> : <Navigate to="/login" replace />}
            />
          </Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
