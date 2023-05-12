import React, { useState, useEffect } from 'react';
import { useRequest } from 'ahooks';
import { BarChartOutlined } from '@ant-design/icons';
import { EditableProTable } from '@ant-design/pro-components';
import { Form, Col, Row, Button, Select, Space, Pagination, Drawer, Card } from 'antd';
import { columns as TrainingColumns } from './columns';
import { getMappingTaskMetaDetail, exportFile } from '../../Mapping/api';
import { PieChart, Pie, BarChart, Bar, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

export default function TrainingMode({ data, taskId, currentPage, onPageChange }) {
  const PAGE_SIZE = 10;
  const [editableKeys, setEditableRowKeys] = useState([]);
  const { data: meta_data } = useRequest(() => getMappingTaskMetaDetail(taskId));

  const num = meta_data?.data.num;
  const num_success = meta_data?.data.num_success;
  const num_failed = meta_data?.data.num_failed;
  const num_reviewed = meta_data?.data.num_reviewed;

  const chartData = [
    { name: 'Success', value: num_success },
    { name: 'Failed', value: num_failed },
    { name: 'Reviewed', value: num_reviewed },
  ];
  
  const transformedChartData = [
    { name: 'Success', Success: num_success },
    { name: 'Failed', Failed: num_failed },
    { name: 'Reviewed', Reviewed: num_reviewed },
  ];

  const renderCustomizedShape = (props) => {
    const { cx, cy, name } = props;
    let fill;
    switch (name) {
      case 'Success':
        fill = 'green';
        break;
      case 'Failed':
        fill = 'red';
        break;
      case 'Reviewed':
        fill = 'orange';
        break;
      default:
        fill = 'gray';
    }
    return <circle cx={cx} cy={cy} r={6} fill={fill} />;
  };

  const [dataSource, setDataSource] = useState(() =>
    data.map((v, i) => {
      return {
        ...v,
        id: i,
      };
    })
  );

  useEffect(() => {
    setDataSource(
      data.map((v, i) => {
        return {
          ...v,
          id: i,
        };
      })
    );
    setEditableRowKeys([]);
  }, [data]);

  const [open, setOpen] = useState(false);
  const showDrawer = () => {
    setOpen(true);
  };

  const onClose = () => {
    setOpen(false);
  };

  const GreenDot = () => {
    const dotGreen = {
      display: 'inline-block',
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: 'green',
      marginRight: '10px',
    };

    return <div style={dotGreen}></div>;
  };

  const RedDot = () => {
    const dotRed = {
      display: 'inline-block',
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: 'red',
      marginRight: '10px',
    };

    return <div style={dotRed}></div>;
  };

  const OrangeDot = () => {
    const dotOrange = {
      display: 'inline-block',
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: 'orange',
      marginRight: '10px',
    };

    return <div style={dotOrange}></div>;
  };

  return (
    <>
      <Form layout="vertical">
        <Row>
          <Col span={16}>
            <Form.Item label="Mapping Status" name="mappingStatus">
              <Select
                style={{ width: 160 }}
                allowClear
                options={[
                  { value: 'success', label: 'Success' },
                  { value: 'fail', label: 'Fail' },
                ]}
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <div class="pt-3 flex justify-end">
              <Space>
                <Button type="primary" size="large">
                  Filter
                </Button>
                <Button size="large">Reset</Button>
                <span class="ml-4">
                  <Button type="primary" size="large" onClick={() => exportFile(taskId)}>
                    Export
                  </Button>
                </span>
                <span class="ml-7 cursor-pointer" onClick={showDrawer}>
                  <BarChartOutlined style={{ fontSize: '23px' }} />
                </span>
              </Space>
            </div>
          </Col>
        </Row>
      </Form>

      {/* <Drawer title="Overall Performance" width={400} onClose={onClose} open={open}>
        <Card
          bordered={false}
          style={{
            width: 300,
          }}
        >
          <div>
            <h4>Total Mapping Text: {num}</h4>
            <h4>Successful Mapping Rate: {num > 0 ? ((num_success / num) * 100).toFixed(2) : 0} %</h4>            
          </div>
          <div>
            <GreenDot />
            Number of Success: {num_success}
          </div>
          <div>
            <RedDot />
            Number of Failure: {num_failed}
          </div>
          <div>
            <OrangeDot />
            Number of Reviewed: {num_reviewed}
          </div>
        </Card>
      </Drawer> */}

      <Drawer title="Overall Performance" width={900} onClose={onClose} open={open}>
        <Row gutter={16}>
          <Col span={12} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <Card
              bordered={true}
              style={{
                width: 300,
              }}
            >
              <div>
                <h4>Total Mapping Text: {num}</h4>
                <h4>Successful Mapping Rate: {num > 0 ? ((num_success / num) * 100).toFixed(2) : 0} %</h4>            
              </div>
              <div>
                <GreenDot />
                Number of Success: {num_success}
              </div>
              <div>
                <RedDot />
                Number of Failure: {num_failed}
              </div>
              <div>
                <OrangeDot />
                Number of Reviewed: {num_reviewed}
              </div>
            </Card>
          </Col>
          <Col span={12} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <PieChart width={400} height={400}>
            <Pie
              data={chartData}
              cx={200}
              cy={200}
              innerRadius={60}
              outerRadius={80}
              fill="#8884d8"
              paddingAngle={5}
              dataKey="value"
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(2)}%`}
              labelLine={false}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.name === 'Success' ? 'green' : entry.name === 'Failed' ? 'red' : 'orange'} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
          </Col>
          <Col span={12} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <BarChart width={400} height={300} data={transformedChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Success" fill="green" />
            <Bar dataKey="Failed" fill="red" />
            <Bar dataKey="Reviewed" fill="orange" />
          </BarChart>
          </Col>
          <Col span={12} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <ScatterChart width={400} height={400} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" type="category" allowDuplicatedCategory={false} />
            <YAxis dataKey="value" type="number" name="value" />
            <Tooltip />
            <Legend />
            <Scatter data={chartData} shape={renderCustomizedShape} line />
          </ScatterChart>
          </Col>
        </Row>
      </Drawer>

      <EditableProTable
        rowKey="id"
        columns={TrainingColumns}
        value={dataSource}
        editable={{
          type: 'multiple',
          editableKeys,
          onSave: async (rowKey, data, row) => {
            // TODO
            console.log(rowKey, data, row);
            data.mappingStatus = 2;
          },
          onChange: setEditableRowKeys,
          actionRender: (row, config, dom) => [dom.save, dom.cancel],
        }}
        onChange={setDataSource}
        maxLength={dataSource.length}
        scroll={{ x: 1200 }}
      />
      {data.length !== 0 && (
        <Pagination
          showQuickJumper
          style={{ display: 'flex', justifyContent: 'flex-end' }}
          current={currentPage}
          // onChange={(page) => setCurrentPage(page)}
          onChange={(page) => onPageChange(page)}
          pageSize={PAGE_SIZE}
          total={num}
          showSizeChanger={false}
        />
      )}
    </>
  );
}
