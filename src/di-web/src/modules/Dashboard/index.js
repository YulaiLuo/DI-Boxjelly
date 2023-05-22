import React, { useState, useRef } from 'react';
import { Col, Row, Input, Spin, Modal } from 'antd';
import { Column } from '@ant-design/plots';
import { useRequest } from 'ahooks';
import { mapSingleText } from '../Mapping/api';
import DashboardCard from './components/DashboardCard';
import { getDashboardInfo, getBarChartInfo, getHelloInfo } from './api';

const { Search } = Input;

export default function Dashboard() {
  const [showSingleMapping, setShowSingleMapping] = useState(false);
  const [singleMappingResult, setSingleMappingResult] = useState('');

  // ref of single text search input
  const inputRef = useRef(null);

  const { loading: singleMapLoading, run: handleMapSingleText } = useRequest(mapSingleText, {
    manual: true,
    onSuccess: (res) => {
      if (res.data.result['0'] && res.data.result['0'] != null) {
        const term = res.data.result['0']['name'];
        const ontology = res.data.result['0']['ontology'];
        const singleResult = [ontology, term];
        setSingleMappingResult(singleResult);
      } else {
        setSingleMappingResult('No mapping result');
      }
    },
  });

  const { data: dashboardInfoResponse } = useRequest(getDashboardInfo);
  const { data: dashboardBarChartResponse } = useRequest(getBarChartInfo);
  const { data: dashboardHelloInfoResponse } = useRequest(getHelloInfo);

  const dashboardInfo = dashboardInfoResponse?.map((res) => res?.data);

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

  const config = {
    data: dashboardBarChartResponse?.data ?? [],
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
                    <div class="text-xl">{singleMappingResult[0]}</div>
                    <div class="text-xl">{singleMappingResult[1]}</div>
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
