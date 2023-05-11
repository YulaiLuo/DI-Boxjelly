import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { List, Pagination, Button, Modal } from 'antd';
import { useRequest } from 'ahooks';
import { getAllMappingTasks, getMappingTaskDetail } from './api';
import TaskCard from './components/TaskCard';
import { Spin } from '../../components';
import { convertKeysToCamelCase } from '../../utils/underlineToCamel';
import { exportFile } from '../Mapping/api';
import { FileUploader } from '../../components';
import { useMessageStore } from '../../store';
import { createMappingTask } from '../Mapping/api';

export default function MappingHistory() {
  const team_id = '60c879e72cb0e6f96d6b0f65';
  const board_id = '60c879e72cb0e6f96d6b0f65';
  const PAGE_SIZE = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const navigate = useNavigate();
  const msgApi = useMessageStore((state) => state.msgApi);

  const onGetTaskDetailSuccess = (data) => {
    console.log('data', data);
    const id = data.data?.id;
    navigate('/mapping-result', { state: { id, team_id, board_id } });
  };

  const { data, loading } = useRequest(
    () => getAllMappingTasks(team_id, board_id, currentPage, PAGE_SIZE),
    {
      refreshDeps: [currentPage],
    }
  );

  const { run: onTaskEditClick } = useRequest(getMappingTaskDetail, {
    manual: true,
    onSuccess: onGetTaskDetailSuccess,
  });

  const tasks = data?.data?.tasks ?? [];
  const mappedTasks = tasks.map((task) => {
    return convertKeysToCamelCase(task);
  });
  const [files, setFiles] = useState([]);

  const [open, setOpen] = useState(false);
  const showModal = () => {
    setOpen(true);
  };
  const handleCancel = () => {
    setOpen(false);
  };

  const { loading: createTaskLoading, run: handleCreateMappingTask } = useRequest(
    createMappingTask,
    {
      manual: true,
      onSuccess: () => {
        setOpen(false);
        msgApi.success('Mapping task created successfully');
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      },
    }
  );

  const onCreateTaskClick = async () => {
    const uploadedFile = files[0]?.file;
    // TODO: currently cannot access the real teamId
    const teamId = '60c879e72cb0e6f96d6b0f65';
    const boardId = '60c879e72cb0e6f96d6b0f65';
    handleCreateMappingTask(uploadedFile, teamId, boardId);
  };

  const onFileUpdate = (files) => {
    setFiles(files);
  };

  return (
    <div class="p-4 h-full">
      {loading ? (
        <Spin />
      ) : (
        <div>
          <div class="flex flex-row-reverse mb-4 mt-2">
            <Button type="primary" onClick={showModal}>
              Create Task
            </Button>
            <Modal
              title="Create Mapping Task"
              open={open}
              onOk={onCreateTaskClick}
              confirmLoading={createTaskLoading}
              onCancel={handleCancel}
            >
              <FileUploader files={files} onFileUpdate={onFileUpdate} />
            </Modal>
          </div>
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
            dataSource={mappedTasks}
            renderItem={(item) => (
              <List.Item>
                <TaskCard
                  item={item}
                  onEditClick={() => onTaskEditClick(item.id, team_id, board_id)}
                  onDownloadClick={() => exportFile(item.id)}
                />
              </List.Item>
            )}
          />
          {tasks.length !== 0 && (
            <div class="flex flex-row-reverse">
              <Pagination
                showQuickJumper
                current={currentPage}
                onChange={(page) => setCurrentPage(page)}
                pageSize={PAGE_SIZE}
                total={PAGE_SIZE * data.data?.page_num}
                showSizeChanger={false}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
