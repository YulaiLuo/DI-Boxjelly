import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useRequest } from 'ahooks';
import TrainingMode from './TrainingMode';
import { getMappingTaskDetail } from '../Mapping/api';

// This component displays the mapping results of a task
export default function MappingResult() {
  const PAGE_SIZE = 20;

  // State variables
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(PAGE_SIZE);

  const navigate = useNavigate();
  const { state } = useLocation();
  const taskId = state.id;
  const teamId = state.team_id;
  const boardId = state.board_id;

  const formRef = useRef();

  // Custom hook for making request to get mapping task detail
  const {
    data,
    loading,
    run: runFilterTaskDetail,
  } = useRequest(getMappingTaskDetail, {
    manual: true, // Indicates that the request will not run automatically
  });

  // Mapping data received from the request
  const mappedItems = data?.data.items ?? [];
  const totalNumber = data?.data.total;

  // Transform the received data into the needed format
  const transformedItems = mappedItems.map((item) => {
    // Some transformations here...
    const mappingStatus = item.status !== 'fail' ? (item.status === 'success' ? 1 : 2) : 0;
    const source = item.ontology;
    const uilStatus = item.extra?.['2']?.value;
    const confidence =
      (item.status !== 'fail' && source !== 'UIL') || uilStatus === 'UIL'
        ? Number(item.accuracy * 100).toFixed(2) + '%'
        : null;

    return {
      originalText: item.text,
      mappedText: item.mapped_concept,
      curate: item.curate,
      confidence,
      source,
      mappingStatus,
      mappedItemId: item.map_item_id,
    };
  });

  // Function to handle filter operation
  const onFilter = () => {
    setCurrentPage(1);
    const filterForm = formRef.current?.form;
    const values = filterForm.getFieldsValue();

    const filter = {
      ...values,
      minConfidence: values.confidence && values.confidence[0] / 100,
      maxConfidence: values.confidence && values.confidence[1] / 100,
    };

    runFilterTaskDetail(taskId, teamId, boardId, 1, pageSize, filter);
  };

  // Function to handle reset operation
  const onReset = () => {
    setCurrentPage(1);
    const filterForm = formRef.current?.form;
    filterForm.setFieldsValue({
      mappingStatus: undefined,
      source: undefined,
      confidence: undefined,
    });
    runFilterTaskDetail(taskId, teamId, boardId, 1, pageSize);
  };

  // Function to handle page change operation
  const handlePageChange = (page, curPageSize) => {
    setCurrentPage(page);
    setPageSize(curPageSize);
    const filterForm = formRef.current?.form;
    const values = filterForm.getFieldsValue();
    const filter = {
      ...values,
      minConfidence: values.confidence && values.confidence[0] / 100,
      maxConfidence: values.confidence && values.confidence[1] / 100,
    };
    runFilterTaskDetail(taskId, teamId, boardId, page, curPageSize, filter);
  };

  // Run initial operations when component is mounted
  useEffect(() => {
    if (state === null) {
      navigate('/', { replace: true });
    }
    runFilterTaskDetail(taskId, teamId, boardId, currentPage, pageSize);
    // eslint-disable-next-line
  }, []);

  // Render the component
  return (
    <div class="px-8 py-4">
      <TrainingMode
        ref={formRef}
        data={transformedItems}
        taskId={taskId}
        currentPage={currentPage}
        isTableLoading={loading}
        totalNumber={totalNumber}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onFilter={onFilter}
        onReset={onReset}
      />
    </div>
  );
}
