import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { useRequest } from 'ahooks';
import { BarChartOutlined, DownloadOutlined } from '@ant-design/icons';
import { EditableProTable } from '@ant-design/pro-components';
import { Form, Col, Row, Button, Select, Space, Pagination, Slider } from 'antd';
import { getColumns } from './columns';
import { getMappingTaskMetaDetail, exportFile, curateMapping } from '../../Mapping/api';
import { VisualizationDrawer } from '../../../components';
import { getCodeSystemList } from '../../CodeSystem/api';

const TrainingMode = forwardRef((props, ref) => {
  const {
    data,
    taskId,
    currentPage,
    isTableLoading,
    totalNumber,
    pageSize,
    onPageChange,
    onFilter,
    onReset,
  } = props;

  const team_id = localStorage.getItem('team');

  const [filterForm] = Form.useForm();

  useImperativeHandle(ref, () => ({
    form: filterForm,
  }));

  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async () => {
    setIsExporting(true);
    try {
      await exportFile(team_id, taskId);
    } catch (error) {
      console.error(error);
    } finally {
      setIsExporting(false);
    }
  };

  const [editableKeys, setEditableRowKeys] = useState([]);
  const { data: meta_data } = useRequest(() => getMappingTaskMetaDetail(taskId));
  const { data: codeSystemList } = useRequest(getCodeSystemList, {
    initialData: [],
  });
  const { run: runCurateMapping } = useRequest(curateMapping, {
    manual: true,
  });

  const mappedCodeSystemList = codeSystemList?.data?.groups?.map((item) => {
    return {
      value: item.group_name,
      label: item.group_name,
      children: item.concept_versions.map((child) => ({
        value: child.concept_name,
        label: child.concept_name,
      })),
    };
  });

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
    <div class="h-[calc(100vh-95px)] relative">
      <Form layout="vertical" form={filterForm}>
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
          <Col xs={24} sm={24} md={12} lg={12} xl={4}>
            <Form.Item label="Source" name="source">
              <Select
                style={{ width: 160 }}
                allowClear
                options={[
                  { value: 'SNOMED-CT', label: 'SNOMED-CT' },
                  { value: 'UIL', label: 'UIL' },
                ]}
              />
            </Form.Item>
          </Col>
          <Col xs={24} sm={24} md={12} lg={12} xl={4}>
            <Form.Item label="Confidence Range" name="confidence">
              <Slider style={{ width: 160 }} range defaultValue={[0, 100]} />
            </Form.Item>
          </Col>
          <Col xs={24} sm={24} md={12} lg={12} xl={8}>
            <div class="pt-3 flex flex-row-reverse">
              <Space>
                <Button type="primary" size="large" onClick={onFilter}>
                  Filter
                </Button>
                <Button size="large" onClick={onReset}>
                  Reset
                </Button>
                <span class="ml-4">
                  <Button
                    type="primary"
                    size="large"
                    onClick={handleExport}
                    icon={<DownloadOutlined />}
                    disabled={isExporting}
                  >
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
        loading={isTableLoading}
        columns={getColumns(mappedCodeSystemList)}
        value={dataSource}
        editable={{
          type: 'multiple',
          editableKeys,
          onSave: async (rowKey, data, row) => {
            data.mappingStatus = 2;
            runCurateMapping(data.mappedItemId, data.curate[1], codeSystemList?.data?.version);
          },
          onChange: setEditableRowKeys,
          actionRender: (row, config, dom) => [dom.save, dom.cancel],
        }}
        onChange={setDataSource}
        maxLength={dataSource.length}
        scroll={{ x: 1200, y: 'calc(100vh - 310px)' }}
      />

      {data.length !== 0 && (
        <div class="absolute bottom-2 right-0">
          <Pagination
            showQuickJumper
            current={currentPage}
            onChange={(page, pageSize) => onPageChange(page, pageSize)}
            pageSize={pageSize}
            total={totalNumber}
          />
        </div>
      )}
    </div>
  );
});

export default TrainingMode;
