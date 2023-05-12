import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Col, Row, Button, Input, Spin } from 'antd';
import { useRequest } from 'ahooks';
import { FileUploader } from '../../components';
import { mapSingleText } from '../Mapping/api';
import { useMessageStore } from '../../store';

const { Search } = Input;

export default function Dashboard() {
  const [showSingleMapping, setShowSingleMapping] = useState(false);
  const [singleMappingResult, setSingleMappingResult] = useState('');

  // ref of single text search input
  const inputRef = useRef(null);

  const { loading: singleMapLoading, run: handleMapSingleText } = useRequest(mapSingleText, {
    manual: true,
    onSuccess: (res) => {
      if (res.data['0'] && res.data['0'].length > 0) {
        setSingleMappingResult(res.data['0'][0].sct_term);
      } else {
        setSingleMappingResult('No mapping result');
      }
    },
  });

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

  return (
    // <div>
    //   <div>
    //
    //   </div>
    //   <div>Current Tasks to do</div>
    //   <div>total Mapping</div>
    // </div>
    <div>
      {/* <h1 className='text-2xl'>Hi! Vlada!</h1> */}
      <Row>
        <Col xs={2} sm={2} md={3} lg={4} xl={5} />
        <Col xs={20} sm={20} md={18} lg={16} xl={14}>
          <div class="pt-6">
            <div class="mt-16 mb-14 text-center text-slate-500 text-2xl">Mapping:</div>
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
    </div>
  );
}
