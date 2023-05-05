import React, { useState } from 'react';
import { List, Pagination } from 'antd';
import { useRequest } from 'ahooks';
import { getAllMappingTasks } from './api';
import TaskCard from './components/TaskCard';
import { Spin } from '../../components';

export default function MappingHistory() {
  const PAGE_SIZE = 4;
  const [currentPage, setCurrentPage] = useState(1);

  const { data, loading } = useRequest(() => getAllMappingTasks(currentPage, PAGE_SIZE), {
    refreshDeps: [currentPage],
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
