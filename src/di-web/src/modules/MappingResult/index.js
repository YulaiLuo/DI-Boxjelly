import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Tabs } from 'antd';
import { useRequest } from 'ahooks';
import InferenceMode from './InferenceMode';
import TrainingMode from './TrainingMode';
import { getMappingTaskDetail } from '../Mapping/api';

export default function MappingResult() {
  const PAGE_SIZE = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const handlePageChange = (page) => {
    console.log(page)
    setCurrentPage(page);
  };
  const navigate = useNavigate();
  const { state } = useLocation();
  const defaultActiveKey = state.mappingMode === 1 ? 'training' : 'inference';
  // TODO: should get mappingRes from backend
  const taskId = state.id;
  const { data, loading } = useRequest(() => getMappingTaskDetail(taskId, currentPage, PAGE_SIZE), {
    refreshDeps: [currentPage],
  });

  const mappedItems = data?.data.items ?? [];

  // TODO: wait for backend response update
  const transformedItems = mappedItems.map((item) => {
    const mappedInfo = item.mapped_info[0];
    const mappingStatus = mappedInfo ? 1 : 0;
    const source = mappedInfo ? 'SNOMED_CT' : null;
    const confidence = mappedInfo ? Number(mappedInfo.confidence * 100).toFixed(2) + '%' : null;

    return {
      originalText: item.text,
      mappedText: mappedInfo?.sct_term,
      curate: null,
      confidence,
      source,
      mappingStatus,
    };
  });

  const items = [
    {
      key: 'inference',
      label: `Inference`,
      children: <InferenceMode data={transformedItems} taskId={taskId} currentPage={currentPage} onPageChange={handlePageChange}/>,
    },
    {
      key: 'training',
      label: `Training`,
      children: <TrainingMode data={transformedItems} taskId={taskId} currentPage={currentPage} onPageChange={handlePageChange}/>,
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
