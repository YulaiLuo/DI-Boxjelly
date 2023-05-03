import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Col, Row, Button, Input, Spin } from 'antd';
import { useRequest } from 'ahooks';
import { FileUploader } from '../../components';
import { mapSingleText, createMappingTask } from './api';
import { useMessageStore } from '../../store';

const { Search } = Input;

export default function Mapping() {
  const msgApi = useMessageStore((state) => state.msgApi);
  const navigate = useNavigate();

  const [files, setFiles] = useState([]);
  const [showSingleMapping, setShowSingleMapping] = useState(false);
  const [singleMappingResult, setSingleMappingResult] = useState('');

  // ref of single text search input
  const inputRef = useRef(null);

  const { loading: singleMapLoading, run: handleMapSingleText } = useRequest(mapSingleText, {
    manual: true,
    onSuccess: (res) => {
      setSingleMappingResult(res.display);
    },
  });

  const { loading: createTaskLoading, run: handleCreateMappingTask } = useRequest(
    createMappingTask,
    {
      manual: true,
      onSuccess: (res) => {
        const id = res.data?.id;
        msgApi.success('Mapping task created successfully');
        navigate('/mapping-result', { state: { id } });
      },
    }
  );

  const onCreateTaskClick = async () => {
    const uploadedFile = files[0]?.file;
    // TODO: currently cannot access the real teamId
    const teamId = '1234';
    handleCreateMappingTask(uploadedFile, teamId);
  };

  const onSingleTextSearch = (value) => {
    if (value.trim() !== '') {
      setShowSingleMapping(true);
      handleMapSingleText(value);
    }
  };

  const onSingleTextChange = (e) => {
    const input = e.target.value;
    if (input.trim() === '') {
      setShowSingleMapping(false);
    }
  };

  const onFileUpdate = (files) => {
    setFiles(files);
  };

  return (
    <Row>
      <Col xs={2} sm={2} md={3} lg={4} xl={5} />
      <Col xs={20} sm={20} md={18} lg={16} xl={14}>
        <div class="pt-6">
          <div class="flex justify-between items-center mb-5">
            <Button
              type="primary"
              size="large"
              disabled={!files.length}
              onClick={onCreateTaskClick}
              loading={createTaskLoading}
            >
              Create a Task
            </Button>
          </div>
          <FileUploader files={files} onFileUpdate={onFileUpdate} />
          <div class="mt-16 mb-14 text-center text-slate-400 text-lg">
            Or input a single text for test
          </div>
          <Search
            placeholder="Input a single text"
            allowClear
            onSearch={onSingleTextSearch}
            ref={inputRef}
            onChange={onSingleTextChange}
          />
          {showSingleMapping && (
            <div class="mt-12 w-full flex justify-center">
              {singleMapLoading ? (
                <Spin />
              ) : (
                <div class="text-center">
                  <div class="mb-4 text-lg">Mapping Result:</div>
                  <div class="text-2xl">{singleMappingResult}</div>
                </div>
              )}
            </div>
          )}
        </div>
      </Col>
      <Col xs={2} sm={2} md={3} lg={4} xl={5} />
    </Row>
  );
}
