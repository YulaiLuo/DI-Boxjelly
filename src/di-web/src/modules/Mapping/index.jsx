import React, { useState, useRef } from 'react';
import { Col, Row, Button, Radio, Input, Spin } from 'antd';
import { FileUploader } from '../../components';

const { Search } = Input;

export default function Mapping() {
  // 0: Inference mode; 1: Training mode
  const [mappingMode, setMappingMode] = useState(0);
  const [files, setFiles] = useState([]);
  const [showSingleMapping, setShowSingleMapping] = useState(false);
  const [singleMappingLoading, setSingleMappingLoading] = useState(false);
  const [singleMappingResult, setSingleMappingResult] = useState('');

  // ref of single text search input
  const inputRef = useRef(null);

  const onSingleTextSearch = (value) => {
    if (value.trim() !== '') {
      setShowSingleMapping(true);
      console.log(`Map ${value}`);
      setSingleMappingLoading(true);
      // TODO: single text mapping
      new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve('this is the mapping result');
        }, 1000);
      })
        .then((res) => {
          setSingleMappingLoading(false);
          setSingleMappingResult(res);
        })
        .catch((err) => {
          setSingleMappingResult('Failed to Map!');
        });
    }else {
      setShowSingleMapping(false);
    }
  };

  const onSingleTextChange = (e) => {
    const input = e.target.value;
    if (input.trim() === '') {
      setShowSingleMapping(false);
    }
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
              <Button type="primary" size="large" disabled={!files.length} block>
                Map
              </Button>
            </div>
          </div>
          <FileUploader files={files} onFileUpdate={setFiles} />
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
              {singleMappingLoading ? (
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
