import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Col, Row, Button, Radio, Input, Spin } from 'antd';
import Papa from 'papaparse';
import { useRequest } from 'ahooks';
import { FileUploader } from '../../components';
import { mapSingleText, mapMultipleText } from './api';
import { useMessageStore } from '../../store';

const { Search } = Input;

export default function Mapping() {
  const msgApi = useMessageStore((state) => state.msgApi);
  const navigate = useNavigate();

  // 0: Inference mode; 1: Training mode
  const [mappingMode, setMappingMode] = useState(0);
  const [files, setFiles] = useState([]);
  const [showSingleMapping, setShowSingleMapping] = useState(false);
  const [singleMappingResult, setSingleMappingResult] = useState('');

  // ref of single text search input
  const inputRef = useRef(null);

  const { loading: multiMapLoading, run: handleMapMultipleText } = useRequest(mapMultipleText, {
    manual: true,
    onSuccess: (res, params) => {
      // TODO: OntoServer api does not return the original text in the response data
      const mappingRes = res.map((v, i) => {
        return {
          ...v,
          originalDisplay: params[0][i],
          // TODO: fake data
          curatedCategory: null,
        };
      });
      msgApi.success('Mapping successfully');
      navigate('/mapping-result', { state: { mappingMode, mappingRes } });
    },
  });

  const { loading: singleMapLoading, run: handleMapSingleText } = useRequest(mapSingleText, {
    manual: true,
    onSuccess: (res) => {
      setSingleMappingResult(res.display);
    },
  });

  const onMapClick = () => {
    Papa.parse(files[0]?.file, {
      header: true,
      skipEmptyLines: true,
      complete: function (results) {
        if (!results.data.length) {
          msgApi.error('There is no data in CSV file!');
          return;
        }
        if (results.data[0].Text === undefined) {
          msgApi.error('Wrong CSV format! The header of the CSV file must include Text');
          return;
        }
        const textArray = results.data.map((v) => v.Text);
        handleMapMultipleText(textArray);
      },
    });
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
            <div>
              <div class="mb-1 text-lg">Select the mode</div>
              <Radio.Group onChange={(e) => setMappingMode(e.target.value)} value={mappingMode}>
                <Radio value={0}>Inference</Radio>
                <Radio value={1}>Training</Radio>
              </Radio.Group>
            </div>
            <div class=" w-24">
              <Button
                type="primary"
                size="large"
                disabled={!files.length}
                block
                onClick={onMapClick}
                loading={multiMapLoading}
              >
                Map
              </Button>
            </div>
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
