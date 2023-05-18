import React, { useState, useRef, useEffect } from 'react';
import { Col, Row, Input, Spin, Avatar, Card, Modal, Button } from 'antd';
import { useRequest } from 'ahooks';
import { mapSingleText } from '../Mapping/api';
import DashboardCard from './components/DashboardCard';
import { Column } from '@ant-design/plots';
import MessageCard from './components/MessageCard';
import { BASE_URL } from '../../utils/constant/url';
import { getDashboardInfo } from './api';

const { Search } = Input;

export default function Dashboard() {
  const [showSingleMapping, setShowSingleMapping] = useState(false);
  const [singleMappingResult, setSingleMappingResult] = useState('');

  const user = JSON.parse(localStorage.getItem('userDetail'));

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

  const { data: dashboardInfoResponse } = useRequest(getDashboardInfo);

  const dashboardInfo = dashboardInfoResponse?.map((res) => res?.data);
  console.log(dashboardInfo);

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
  const [data, setData] = useState([]);

  useEffect(() => {
    asyncFetch();
  }, []);

  const asyncFetch = () => {
    fetch('https://gw.alipayobjects.com/os/antfincdn/8elHX%26irfq/stack-column-data.json')
      .then((response) => response.json())
      .then((json) => setData(json))
      .catch((error) => {
        console.log('fetch data failed', error);
      });
  };
  const config = {
    data,
    isStack: true,
    xField: 'year',
    yField: 'value',
    seriesField: 'type',
    label: {
      // 可手动配置 label 数据标签位置
      position: 'middle',
      // 'top', 'bottom', 'middle'
      // 可配置附加的布局方法
      layout: [
        // 柱形图数据标签位置自动调整
        {
          type: 'interval-adjust-position',
        }, // 数据标签防遮挡
        {
          type: 'interval-hide-overlap',
        }, // 数据标签文颜色自动调整
        {
          type: 'adjust-color',
        },
      ],
    },
  };

  const [isModalOpen, setIsModalOpen] = useState(false);

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  return (
    // <div>
    //   <div>
    //
    //   </div>
    //   <div>Current Tasks to do</div>
    //   <div>total Mapping</div>
    // </div>

    <div style={{ display: 'flex', height: '100%' }}>
      <div class="mx-8 pt-4 flex-1">
        <Row>
          <Col xs={24} sm={24} md={12} lg={12} xl={12}>
            <div>
              <h1 class="">Dashboard</h1>
              <div>Hello, {user?.nickname}. Welcome!</div>
            </div>
          </Col>

          <Col xs={24} sm={24} md={12} lg={{ span: 6, offset: 6 }} xl={{ span: 6, offset: 6 }}>
            <div class="h-full flex items-center">
              <Search
                placeholder="Input a single text"
                allowClear
                onSearch={onSingleTextSearch}
                //onSearch = {showModal}
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
                    <div class="text-2xl">{singleMappingResult}</div>
                  </div>
                )}
              </div>
            )}
          </Modal>
        </Row>

        <div class="mt-5">
          <Row gutter={[24, 8]}>
            {dashboardInfo?.map((item) => (
              <Col xs={24} sm={24} md={12} lg={8} xl={8}>
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

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
          width: 300,
          background: 'White',
        }}
      >
        <div
          style={{
            // background: 'White',
            textAlign: 'center',
            // alignItems: 'center',
            // position: 'absolute',
            // right: 0,
            // top: 0,
            // bottom: 0,
          }}
        >
          <Avatar
            // class="mt-4"
            src={`${BASE_URL}/auth/user/avatar?avatar=${user.avatar}`}
            style={{
              width: '150px',
              height: '150px',
              marginTop: '100px',
              marginLeft: 'auto',
              marginRight: 'auto',
            }}
          />
          <div>
            <h3>{user?.nickname}</h3>
          </div>
          <div style={{ marginTop: '20px' }}>
            <h3>Recent Task</h3>
            <Card
              size="small"
              extra={null}
              style={{ height: 100, width: 250, marginLeft: 'auto', marginRight: 'auto' }}
            >
              <h4>Task Name</h4>
              <p>Task Info</p>
            </Card>
          </div>
          <div style={{ marginTop: '20px' }}>
            <h3>Messages </h3>
            <MessageCard />
            <MessageCard />
          </div>
        </div>
      </div>
    </div>
  );
}
