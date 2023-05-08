import React, { useState, useEffect } from 'react';
import { BarChartOutlined } from '@ant-design/icons';
import { EditableProTable } from '@ant-design/pro-components';
import { Form, Col, Row, Button, Select, Space, Pagination, Drawer, Card } from 'antd';
import { columns as TrainingColumns } from './columns';

export default function TrainingMode({ data, taskId, page_num, currentPage, onPageChange }) {
  const PAGE_SIZE = 10;
  const [editableKeys, setEditableRowKeys] = useState([]);
  
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
        }
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

  const numberOfSuccess = useState(() => {
    return dataSource.filter((item) => item.mappingStatus === 1).length;
  }, [dataSource]);

  const numberOfFail = useState(() => {
    return dataSource.filter((item) => item.mappingStatus === 0).length;
  }, [dataSource]);

  const totalNumber = useState(() => {
    return dataSource.filter((item) => item.mappingStatus === 1).length + dataSource.filter((item) => item.mappingStatus === 0).length;
  }, [dataSource]);

  const SuccessfulMappingRate = useState(() => {
    const successfulMappings = dataSource.filter((item) => item.mappingStatus === 1).length;
    const totalMappings = successfulMappings + dataSource.filter((item) => item.mappingStatus === 0).length;
    const rate = totalMappings > 0 ? (successfulMappings / totalMappings) * 100 : 0;
    return parseFloat(rate.toFixed(2));
  }, [dataSource]);

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
  
  return (
    <>
      <Form layout="vertical">
        <Row>
          <Col span={18}>
            <Form.Item label="Mapping Status" name="mappingStatus">
              <Select
                style={{ width: 160 }}
                allowClear
                options={[
                  { value: 'success', label: 'success' },
                  { value: 'fail', label: 'fail' },
                ]}
              />
            </Form.Item>
          </Col>
          <Col span={6}>
            <div class="pt-3">
              <Space>
                <Button type="primary" size="large">
                  Filter
                </Button>
                <Button size="large">Reset</Button>
                <span class="ml-7 cursor-pointer" onClick={showDrawer}>
                  <BarChartOutlined style={{ fontSize: '23px' }} />
                </span>
              </Space>              
            </div>
          </Col>
        </Row>
      </Form>
      
      <Drawer
        title="Overall Performance"
        width={400}
        onClose={onClose}
        open={open}
      >
        <Card
          bordered={false}
          style={{
            width: 300,
          }}
        >
          <h2>Total Mapping Text: {totalNumber}</h2>
          <div>
            <GreenDot />
            Number of Success: {numberOfSuccess}
          </div>
          <div>
            <RedDot />
            Number of failure: {numberOfFail}
          </div>
        </Card>
        <h2>Successful mapping rate: {SuccessfulMappingRate} %</h2>
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
          current={currentPage}
          // onChange={(page) => setCurrentPage(page)}
          onChange={(page) => onPageChange(page)}
          pageSize={PAGE_SIZE}
          total={PAGE_SIZE * page_num}
        />
      )}
    </>
  );
}
