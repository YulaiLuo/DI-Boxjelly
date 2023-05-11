import React, { useState, useEffect } from 'react';
import { useRequest } from 'ahooks';
import { BarChartOutlined } from '@ant-design/icons';
import { EditableProTable } from '@ant-design/pro-components';
import { Form, Col, Row, Button, Select, Space, Pagination, Drawer, Card } from 'antd';
import { columns as TrainingColumns } from './columns';
import { getMappingTaskMetaDetail, exportFile } from '../../Mapping/api';
import { PieChart, Pie, Cell } from 'recharts';

export default function TrainingMode({ data, taskId, currentPage, onPageChange }) {
  const PAGE_SIZE = 10;
  const [editableKeys, setEditableRowKeys] = useState([]);
  const { data: meta_data } = useRequest(() => getMappingTaskMetaDetail(taskId));

  const num = meta_data?.data.num;
  const num_success = meta_data?.data.num_success;
  const num_failed = meta_data?.data.num_failed;
  const num_reviewed = meta_data?.data.num_reviewed;

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

  // const numberOfSuccess = useState(() => {
  //   return dataSource.filter((item) => item.mappingStatus === 1).length;
  // }, [dataSource]);

  // const numberOfFail = useState(() => {
  //   return dataSource.filter((item) => item.mappingStatus === 0).length;
  // }, [dataSource]);

  // const totalNumber = useState(() => {
  //   return (
  //     dataSource.filter((item) => item.mappingStatus === 1).length +
  //     dataSource.filter((item) => item.mappingStatus === 0).length
  //   );
  // }, [dataSource]);

  // const SuccessfulMappingRate = useState(() => {
  //   const successfulMappings = dataSource.filter((item) => item.mappingStatus === 1).length;
  //   const totalMappings =
  //     successfulMappings + dataSource.filter((item) => item.mappingStatus === 0).length;
  //   const rate = totalMappings > 0 ? (successfulMappings / totalMappings) * 100 : 0;
  //   return parseFloat(rate.toFixed(2));
  // }, [dataSource]);

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
            <div class="pt-3">
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

      <Drawer title="Overall Performance" width={400} onClose={onClose} open={open}>
        <Card
          bordered={false}
          style={{
            width: 300,
          }}
        >
          <h2>Total Mapping Text: {num}</h2>
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
        <h2>Successful Mapping Rate: {num > 0 ? ((num_success / num) * 100).toFixed(2) : 0} %</h2>
        {/* <PieChart width={800} height={400}>
          <Pie
            data={aaa}
            cx={200}
            cy={200}
            innerRadius={60}
            outerRadius={80}
            fill="#8884d8"
            paddingAngle={5}
            dataKey="value"
          >
            {
              data.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
            }
          </Pie>
        </PieChart> */}
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
