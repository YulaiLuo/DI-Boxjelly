import React, { useState, useEffect } from 'react';
import { useRequest } from 'ahooks';
import { BarChartOutlined } from '@ant-design/icons';
import { EditableProTable } from '@ant-design/pro-components';
import { Form, Col, Row, Button, Select, Space, Pagination } from 'antd';
import { columns as TrainingColumns } from './columns';
import { getMappingTaskMetaDetail, exportFile } from '../../Mapping/api';
import { VisualizationDrawer } from '../../../components';

export default function TrainingMode({ data, taskId, currentPage, onPageChange }) {
  const PAGE_SIZE = 10;
  const [editableKeys, setEditableRowKeys] = useState([]);
  const { data: meta_data } = useRequest(() => getMappingTaskMetaDetail(taskId));

  const num = meta_data?.data.num;

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

  return (
    <>
      <Form layout="vertical">
        <Row>
          <Col xs={24} sm={24} md={12} lg={12} xl={4}>
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

          <Col xs={24} sm={24} md={12} lg={12} xl={12}>
            <Form.Item label="Source" name="source">
              <Select
                style={{ width: 160 }}
                allowClear
                options={[
                  { value: 'SNOMED_CT', label: 'SNOMED_CT' },
                  { value: 'UIL', label: 'UIL' },
                ]}
              />
            </Form.Item>
          </Col>
          <Col xs={24} sm={24} md={12} lg={24} xl={8}>
            <div class="pt-3 flex flex-row-reverse">
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
      <VisualizationDrawer onClose={onClose} open={open} metaData={meta_data} />
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
