// This module exports the MappingHistory React component, which is responsible for displaying
// a list of all mapping tasks associated with a particular board.
// It provides functionality to create new mapping tasks, navigate to mapping task results,
// visualize task meta-data, and delete mapping tasks.
import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { List, Pagination, Button, Modal } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { useRequest } from 'ahooks';
import { getAllMappingTasks, deleteMappingTask } from './api';
import TaskCard from './components/TaskCard';
import { Spin, VisualizationDrawer } from '../../components';
import { convertKeysToCamelCase } from '../../utils/underlineToCamel';
import { FileUploader } from '../../components';
import { useMessageStore } from '../../store';
import { createMappingTask, getMappingTaskMetaDetail, exportFile } from '../Mapping/api';

export default function MappingHistory() {
  // Various states used in the MappingHistory component.
  const team_id = localStorage.getItem('team');
  const { id: board_id } = useParams();
  const PAGE_SIZE = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [metaData, setMetaData] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [files, setFiles] = useState([]);
  const [open, setOpen] = useState(false);

  // Use the 'useNavigate' and 'useParams' hooks from react-router-dom to navigate between routes
  // and fetch URL parameters respectively.
  const navigate = useNavigate();
  const msgApi = useMessageStore((state) => state.msgApi);

  // Function executed on successful task detail retrieval. Navigates to the 'mapping-result' route.
  const onGetTaskDetailSuccess = (id, team_id, board_id) => {
    navigate('/mapping-result', { state: { id, team_id, board_id } });
  };

  // Fetch all mapping tasks associated with the current board.
  const { data, loading } = useRequest(
    () => getAllMappingTasks(team_id, board_id, currentPage, PAGE_SIZE),
    {
      refreshDeps: [currentPage, board_id, team_id],
    }
  );

  // Execute the 'getMappingTaskMetaDetail' function when the visualization button is clicked.
  const { run: onVisualizationClick } = useRequest(getMappingTaskMetaDetail, {
    manual: true,
    onSuccess: (data) => {
      setMetaData(data);
    },
  });

  // Execute the 'deleteMappingTask' function when the delete button is clicked. On successful
  // deletion, a success message is displayed and the page is refreshed.
  const { run: onTaskDeleteClick } = useRequest(deleteMappingTask, {
    manual: true,
    onSuccess: (data) => {
      msgApi.success('Mapping task deleted successfully');
      setTimeout(() => {
        window.location.reload();
      }, 1000);
    },
  });

  const tasks = data?.data?.tasks ?? [];
  const boardDescription = data?.data?.board_description;
  const boardName = data?.data?.board_name;

  // Convert the keys of the fetched task data from snake case to camel case for consistency.
  const mappedTasks = tasks.map((task) => {
    return convertKeysToCamelCase(task);
  });

  // Functions for handling the opening and closing of the modal.
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

  // Create a mapping task when the "Create Task" button is clicked.
  const onCreateTaskClick = async (team_id, board_id) => {
    const uploadedFile = files[0]?.file;
    handleCreateMappingTask(team_id, board_id, uploadedFile);
  };

  const onFileUpdate = (files) => {
    setFiles(files);
  };

  return (
    // JSX for the MappingHistory component.
    <div class="p-4 ">
      {loading ? (
        <Spin />
      ) : (
        <div class="h-[calc(100vh-95px)] relative">
          <VisualizationDrawer
            onClose={() => setDrawerOpen(false)}
            open={drawerOpen}
            metaData={metaData}
          />
          <div class="flex justify-between items-center mb-6 mt-2">
            <div>
              <div class="text-xl mb-2">{boardName}</div>
              <span class="text-gray-500">{boardDescription}</span>
            </div>
            <Button type="primary" onClick={showModal} icon={<PlusOutlined />}>
              Create Task
            </Button>
            <Modal
              title="Create Mapping Task"
              open={open}
              onOk={() => onCreateTaskClick(team_id, board_id)}
              confirmLoading={createTaskLoading}
              onCancel={handleCancel}
            >
              <FileUploader files={files} onFileUpdate={onFileUpdate} />
            </Modal>
          </div>
          <div class="overflow-auto h-[calc(100vh-240px)]">
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
                    onEditClick={() => onGetTaskDetailSuccess(item.id, team_id, board_id)}
                    onDownloadClick={() => exportFile(team_id, item.id)}
                    onVisualizeClick={() => {
                      setDrawerOpen(true);
                      onVisualizationClick(item.id);
                    }}
                    onDeleteClick={() => onTaskDeleteClick(item.id, team_id, board_id)}
                  />
                </List.Item>
              )}
            />
          </div>

          {tasks.length !== 0 && (
            <div class="absolute bottom-2 right-0">
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
