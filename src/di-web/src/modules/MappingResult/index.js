import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Tabs } from 'antd';
import { useRequest } from 'ahooks';
import InferenceMode from './InferenceMode';
import TrainingMode from './TrainingMode';
import { getMappingTaskDetail } from '../Mapping/api';

export default function MappingResult() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const defaultActiveKey = state.mappingMode === 1 ? 'training' : 'inference';
  // TODO: should get mappingRes from backend
  const taskId = state.id;
  const { data, loading } = useRequest(() => getMappingTaskDetail(taskId));
  const mappedItems = data?.data.mappedItems ?? [];

  const items = [
    {
      key: 'inference',
      label: `Inference`,
      children: <InferenceMode data={mappedItems} />,
    },
    {
      key: 'training',
      label: `Training`,
      children: <TrainingMode data={mappedItems} />,
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
