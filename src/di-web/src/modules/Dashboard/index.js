import React, { useState, useRef , useEffect} from 'react';
import { Col, Row, Input, Spin,Avatar, Card } from 'antd';
import { useRequest } from 'ahooks';
import { mapSingleText } from '../Mapping/api';
import DashboardCard from './components/DashboardCard';
import { Column } from '@ant-design/plots';
import MessageCard from './components/MessageCard';

//import Column from 'antd/es/table/Column';
//import React, { useState, useEffect } from 'react';
//import { Column } from '@ant-design/charts';



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
  };const [data, setData] = useState([]);

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


 


  return (
    // <div>
    //   <div>
    //
    //   </div>
    //   <div>Current Tasks to do</div>
    //   <div>total Mapping</div>
    // </div>
  <div style={{ display: 'flex', height: '100%' }}>

    

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

      <div>
        <Column {...config} />
      </div>

      </div>

      

      <div style={{ background: 'White', width: 300 , textAlign: 'center' , alignItems: 'center'}}>
        
        <Avatar
          // class="mt-4"
          src={`https://xsgames.co/randomusers/assets/avatars/pixel/46.jpg`}
          style={{ width: '150px', height: '150px', marginTop: '20px', marginLeft: 'auto', marginRight: 'auto' } }
        />
        <div>
          <h3>Name</h3>
          <p>Title</p>
        </div>
        <div style={{ marginTop: '20px' }}>
          <h3>Recent Task</h3>
          <Card size="small" extra={null} style={{ height: 100 , width: 250 }}>
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


  );
}
