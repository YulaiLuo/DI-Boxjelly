import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useRequest } from 'ahooks';
import TrainingMode from './TrainingMode';
import { getMappingTaskDetail } from '../Mapping/api';

export default function MappingResult() {
  const PAGE_SIZE = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(PAGE_SIZE);

  const navigate = useNavigate();
  const { state } = useLocation();
  const taskId = state.id;
  const teamId = state.team_id;
  const boardId = state.board_id;

  const formRef = useRef();

  const {
    data,
    loading,
    run: runFilterTaskDetail,
  } = useRequest(getMappingTaskDetail, {
    manual: true,
  });

  const mappedItems = data?.data.items ?? [];
  const totalNumber = data?.data.total;

  const transformedItems = mappedItems.map((item) => {
    const mappingStatus = item.status !== 'fail' ? (item.status === 'success' ? 1 : 2) : 0;
    const source = item.ontology;
    const confidence = item.status !== 'fail' ? Number(item.accuracy * 100).toFixed(2) + '%' : null;

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

  useEffect(() => {
    if (state === null) {
      navigate('/', { replace: true });
    }
    runFilterTaskDetail(taskId, teamId, boardId, currentPage, pageSize);
    // eslint-disable-next-line
  }, []);

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
