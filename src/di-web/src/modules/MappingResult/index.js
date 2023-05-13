import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useRequest } from 'ahooks';
import TrainingMode from './TrainingMode';
import { getMappingTaskDetail } from '../Mapping/api';

export default function MappingResult() {
  const PAGE_SIZE = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const handlePageChange = (page) => {
    console.log(page);
    setCurrentPage(page);
  };
  const navigate = useNavigate();
  const { state } = useLocation();
  // TODO: should get mappingRes from backend
  const taskId = state.id;
  const teamId = state.team_id;
  const boardId = state.board_id;
  console.log(state);

  const { data, loading } = useRequest(
    () => getMappingTaskDetail(taskId, teamId, boardId, currentPage, PAGE_SIZE),
    {
      refreshDeps: [currentPage],
    }
  );

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

  useEffect(() => {
    if (state === null) {
      navigate('/', { replace: true });
    }
    // eslint-disable-next-line
  }, []);

  return (
    <div class="px-8 py-4">
      <TrainingMode
        data={transformedItems}
        taskId={taskId}
        currentPage={currentPage}
        onPageChange={handlePageChange}
      />
    </div>
  );
}
