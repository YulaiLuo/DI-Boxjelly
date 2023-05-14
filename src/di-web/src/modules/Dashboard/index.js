import React, { useState, useRef } from 'react';
import { Col, Row, Input, Spin } from 'antd';
import { useRequest } from 'ahooks';
import { mapSingleText } from '../Mapping/api';
import DashboardCard from './components/DashboardCard';

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
    <div class="mx-8 pt-4">
      <Row>
        {/* <h1 className='text-2xl'>Hi! Vlada!</h1> */}
        {/* <Row>

      </Row> */}
        <Col xs={24} sm={24} md={12} lg={12} xl={12}>
          <div>
            <h1 class="">Dashboard</h1>
            <div>Hello, Vlada. Welcome!</div>
          </div>
        </Col>

        <Col xs={24} sm={24} md={12} lg={6} xl={6}>
          <div class="h-full flex items-center">
            <Search
              placeholder="Input a single text"
              allowClear
              onSearch={onSingleTextSearch}
              ref={inputRef}
              onChange={onSingleTextChange}
            />
          </div>
        </Col>

        <Col xs={24} sm={24} md={12} lg={6} xl={6} class="flex items-center">
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
        </Col>

        {/* <Row>
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
        </Row> */}
      </Row>
      <div class="mt-5">
        <Row gutter={[24, 8]}>
          <Col xs={24} sm={24} md={12} lg={8} xl={8}>
            <DashboardCard title="Total xxxx" percent={74} totalNumber={878} />
          </Col>
          <Col xs={24} sm={24} md={12} lg={8} xl={8}>
            <DashboardCard title="Total xxxx" percent={63} totalNumber={343} />
          </Col>
          <Col xs={24} sm={24} md={12} lg={8} xl={8}>
            <DashboardCard title="Total xxxx" percent={25} totalNumber={82} />
          </Col>
        </Row>
      </div>
    </div>
  );
}
