import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Tabs } from 'antd';
import InferenceMode from './InferenceMode';
import TrainingMode from './TrainingMode';

export default function MappingResult() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const defaultActiveKey = state.mappingMode === 1 ? 'training' : 'inference';
  // TODO: should get mappingRes from backend
  const data = state.mappingRes ?? [];

  const items = [
    {
      key: 'inference',
      label: `Inference`,
      children: <InferenceMode data={data} />,
    },
    {
      key: 'training',
      label: `Training`,
      children: <TrainingMode data={data} />,
    },
  ];

  useEffect(() => {
    if (state === null) {
      navigate('/', { replace: true });
    }
    // eslint-disable-next-line
  }, []);

  return (
    <div class="px-8 py-4">
      <Tabs
        defaultActiveKey={defaultActiveKey}
        items={items}
        onChange={() => {}}
        tabBarGutter={30}
      />
    </div>
  );
}
