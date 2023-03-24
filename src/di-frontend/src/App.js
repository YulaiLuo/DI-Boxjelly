import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Login, Mapping, Profile, MappingHistory, RetrainHistory, Dashboard } from './modules';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        {/* <Route path="/" element={<Navigate to="dashboard/mapping"/>} /> */}
        <Route element={<Dashboard />}>
          <Route path="/" element={<Navigate to="/mapping" replace />} />
          <Route path="/mapping" element={<Mapping />} />
          <Route path="/mapping-history" element={<MappingHistory />} />
          <Route path="/retrain-history" element={<RetrainHistory />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
