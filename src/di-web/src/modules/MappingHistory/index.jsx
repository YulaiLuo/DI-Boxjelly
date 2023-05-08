import React, { useState } from 'react';
import { List, Pagination } from 'antd';
import { useRequest } from 'ahooks';
import { getAllMappingTasks, getMappingTaskDetail } from './api';
import TaskCard from './components/TaskCard';
import { Spin } from '../../components';
import { useNavigate } from 'react-router-dom';

export default function MappingHistory() {
  const PAGE_SIZE = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const navigate = useNavigate();
  
  const onGetTaskDetailSuccess = (data) => {
    console.log('data', data);
    const id = data.data?.id;
    navigate('/mapping-result', { state: { id } });
  };

  const { data, loading } = useRequest(() => getAllMappingTasks(currentPage, PAGE_SIZE), {
    refreshDeps: [currentPage],
  });

  const { run: onTaskEditClick } = useRequest(getMappingTaskDetail, {
    manual: true,
    onSuccess: onGetTaskDetailSuccess,
  });

  const tasks = data?.data?.tasks ?? [];
  return (
    <div class="m-4 h-full">
      {loading ? (
        <Spin />
      ) : (
        <>
          <List
            grid={{
              gutter: 25,
              xs: 1,
              sm: 2,
              md: 3,
              lg: 3,
              xl: 4,
              xxl: 5,
            }}
            dataSource={tasks}
            renderItem={(item) => (
              <List.Item>
                <TaskCard
                  id={item.id}
                  status={item.status}
                  num={item.num}
                  createBy={item.create_by}
                  createAt={item.create_at}
                  updateAt={item.update_at}
                  onEditClick={() => onTaskEditClick(item.id)}
                />
              </List.Item>
            )}
          />
          {tasks.length !== 0 && (
            <Pagination
              current={currentPage}
              onChange={(page) => setCurrentPage(page)}
              pageSize={PAGE_SIZE}
              total={PAGE_SIZE * data.data?.page_num}
            />
          )}
        </>
      )}
    </div>
  );
}
