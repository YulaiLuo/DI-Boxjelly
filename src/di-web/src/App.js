import { message } from 'antd';
import { useMessageStore } from './store';
import { BrowserRouter as Router, Routes, Route, Navigate, R } from 'react-router-dom';
import { Login, Mapping, Profile, MappingHistory, RetrainHistory, Dashboard } from './modules';
import { checkAuthentication } from './utils/auth';

function App() {
  // global message display
  const [messageApi, contextHolder] = message.useMessage();
  const setMsgApi = useMessageStore((state) => state.setMsgApi);
  setMsgApi(messageApi);

  const loggedIn = checkAuthentication();

  return (
    <>
      {contextHolder}
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          {/* <Route path="/" element={<Navigate to="dashboard/mapping"/>} /> */}
          <Route element={loggedIn ? <Dashboard /> : <Navigate to="/login" replace />}>
            <Route
              path="/"
              element={
                loggedIn ? <Navigate to="/mapping" replace /> : <Navigate to="/login" replace />
              }
            />
            <Route
              path="/mapping"
              element={loggedIn ? <Mapping /> : <Navigate to="/login" replace />}
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
          </Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
