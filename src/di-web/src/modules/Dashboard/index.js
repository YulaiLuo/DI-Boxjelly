// Importing required dependencies
import React, { useState, useRef } from 'react';
import { Col, Row, Input, Spin, Modal } from 'antd';
import { Column } from '@ant-design/plots';
import { useRequest } from 'ahooks';
import { mapSingleText } from '../Mapping/api';
import DashboardCard from './components/DashboardCard';
import { getDashboardInfo, getBarChartInfo, getHelloInfo } from './api';

const { Search } = Input;

// Main Dashboard component
export default function Dashboard() {
  const [showSingleMapping, setShowSingleMapping] = useState(false);
  const [singleMappingResult, setSingleMappingResult] = useState('');

  // ref of single text search input
  const inputRef = useRef(null);

  // Request handler for mapSingleText API
  const { loading: singleMapLoading, run: handleMapSingleText } = useRequest(mapSingleText, {
    manual: true,
    onSuccess: (res) => {
      // process and update the mapping result state
      if (
        res.data.result['0'] &&
        res.data.result['0'] !== null &&
        res.data.result['0'] !== undefined
      ) {
        const term = res.data.result['0']['name'];
        const ontology = res.data.result['0']['ontology'];
        const singleResult = [ontology, term];
        setSingleMappingResult(singleResult);
      } else {
        setSingleMappingResult('No mapping result');
      }
    },
  });

  // Fetch dashboard info, bar chart info and hello info
  const { data: dashboardInfoResponse } = useRequest(getDashboardInfo);
  const { data: dashboardBarChartResponse } = useRequest(getBarChartInfo);
  const { data: dashboardHelloInfoResponse } = useRequest(getHelloInfo);

  // Processing the response data for rendering
  const dashboardInfo = dashboardInfoResponse?.map((res) => res?.data);
  const toTitleCase = (str) => str.charAt(0).toUpperCase() + str.slice(1);
  const dashboardBarChartResponseTitled = dashboardBarChartResponse?.data.map((item) => ({
    ...item,
    type: toTitleCase(item.type),
  }));

  // Event handlers for single text search
  const onSingleTextSearch = (value) => {
    if (value.trim() !== '') {
      setIsModalOpen(true);

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

  // Chart configuration
  const config = {
    data: dashboardBarChartResponseTitled ?? [],
    isStack: true,
    xField: 'year',
    yField: 'value',
    seriesField: 'type',
    label: {
      position: 'middle',
      layout: [
        {
          type: 'interval-adjust-position',
        },
        {
          type: 'interval-hide-overlap',
        },
        {
          type: 'adjust-color',
        },
      ],
    },
  };

  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOk = () => {
    setIsModalOpen(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  // Rendering the dashboard, search input, modals and chart
  return (
    <div>
      <div class="mx-8 pt-4 flex-1">
        <Row>
          <Col xs={24} sm={24} md={12} lg={12} xl={12}>
            <div>
              <h1 class="">Dashboard</h1>
              <div>
                {dashboardHelloInfoResponse ? dashboardHelloInfoResponse?.data['hello'] : ''}
              </div>
            </div>
          </Col>

          <Col xs={24} sm={24} md={12} lg={{ span: 6, offset: 6 }} xl={{ span: 6, offset: 6 }}>
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

          <Modal title="Mapping Results" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
            {showSingleMapping && (
              <div class="mt-12 w-full flex justify-center">
                {singleMapLoading ? (
                  <Spin />
                ) : (
                  <div class="text-center">
                    {Array.isArray(singleMappingResult) && singleMappingResult.length === 2 ? (
                      <>
                        <div class="text-xl">{singleMappingResult[0]}</div>
                        <div class="text-xl">{singleMappingResult[1]}</div>
                      </>
                    ) : (
                      <div class="text-xl">{singleMappingResult}</div>
                    )}
                  </div>
                )}
              </div>
            )}
          </Modal>
        </Row>

        <div class="mt-5">
          <Row gutter={[24, 8]}>
            {dashboardInfo?.map((item, index) => (
              <Col xs={24} sm={24} md={12} lg={8} xl={8} key={index}>
                <DashboardCard
                  title={item?.title}
                  percent={item?.percent}
                  totalNumber={item?.total_number}
                  delta={item?.delta}
                />
              </Col>
            ))}
          </Row>
        </div>

        <div class="mt-5 bg-white pl-5 py-5">
          <Column {...config} />
        </div>
      </div>
    </div>
  );
}
