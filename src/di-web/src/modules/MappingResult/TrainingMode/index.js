import React, { useState } from 'react';
import { BarChartOutlined } from '@ant-design/icons';
import { EditableProTable } from '@ant-design/pro-components';
import { Form, Col, Row, Button, Select, Space, Pagination } from 'antd';
import { columns as TrainingColumns } from './columns';

export default function TrainingMode({ data }) {
  const [editableKeys, setEditableRowKeys] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [dataSource, setDataSource] = useState(() =>
    data.map((v, i) => {
      return {
        ...v,
        id: i,
      };
    })
  );

  console.log(window.innerHeight);

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
              </Space>
              <span class="ml-7 cursor-pointer">
                <BarChartOutlined style={{ fontSize: '23px' }} />
              </span>
            </div>
          </Col>
        </Row>
      </Form>
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
          onChange={(page) => setCurrentPage(page)}
          pageSize={10}
          total={10 * data.data?.page_num}
        />
      )}
    </>
  );
}
