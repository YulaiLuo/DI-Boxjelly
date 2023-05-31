import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Layout, Menu, Modal, Input, Space, Tooltip, Form, Select, Popconfirm } from 'antd';
import { PlusOutlined, DownloadOutlined } from '@ant-design/icons';
import { useRequest } from 'ahooks';
import CodeCard from './components/CodeCard';
import {
  getCodeSystemList,
  createNewCodeSystem,
  getAllCodeSystemVersion,
  deleteCodeSystem,
  exportCodeSystem,
} from './api';
import { FileUploader, Spin } from '../../components';
import { useMessageStore } from '../../store';

const { Sider, Content } = Layout;

export default function CodeSystem() {
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const [conceptsInGroup, setConceptsInGroup] = useState([]);
  const [allGroups, setAllGroups] = useState([]);
  const [groups, setGroups] = useState([]);
  const [files, setFiles] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const msgApi = useMessageStore((state) => state.msgApi);

  // get code system http request
  const {
    data: codeSystemList,
    loading: getCodeSystemListLoading,
    run: runGetCodeSystemList,
  } = useRequest(getCodeSystemList, {
    initialData: [],
    onSuccess: (data) => {
      const groups = data?.data?.groups ?? [];
      const allGroups = groups
        .reduce((pre, cur) => [...pre, ...cur.concept_versions], [])
        .sort((a, b) => a?.concept_name.localeCompare(b?.concept_name));
      setGroups(groups);
      setConceptsInGroup(allGroups);
      setAllGroups(allGroups);
    },
  });

  // create code system http request
  const { run: runCreateNewCodeSystem, loading: createNewCodeSystemLoading } = useRequest(
    createNewCodeSystem,
    {
      manual: true,
      onSuccess: (data) => {
        setIsModalOpen(false);
        msgApi.success('Updated successfully!');
        runGetAllCodeSystemVersion();
      },
    }
  );

  // delete code system http request
  const { run: runDeleteCodeSystem, loading: deleteCodeSystemLoading } = useRequest(
    deleteCodeSystem,
    {
      manual: true,
      onSuccess: () => {
        msgApi.success('Deleted successfully!');
        runGetCodeSystemList();
        runGetAllCodeSystemVersion();
      },
    }
  );

  const { run: runExportCodeSystem, loading: exportCodeSystemLoading } = useRequest(
    exportCodeSystem,
    {
      manual: true,
    }
  );

  // get all code system versions http request
  const { data: allCodeSystemVersionResponse, run: runGetAllCodeSystemVersion } =
    useRequest(getAllCodeSystemVersion);

  const allCodeSystemVersion = allCodeSystemVersionResponse?.data?.code_systems ?? [];
  const allVersionSelectOptions = allCodeSystemVersion.map((item) => ({
    label: item?.version,
    value: item?.version,
  }));
  const sidebarItems = [
    {
      label: 'All',
      key: 'all',
    },
    ...groups.map((group) => {
      return {
        label: (
          <div class="flex justify-between">
            <Tooltip title={group.group_name}>
              <span className="overflow-hidden overflow-ellipsis">{group?.group_name}</span>
            </Tooltip>
          </div>
        ),
        key: group?.group_name,
      };
    }),
  ];

  const onGroupItemClick = (groupName) => {
    const group = groups
      .find((item) => item.group_name === groupName)
      ?.concept_versions.sort((a, b) => a?.concept_name.localeCompare(b?.concept_name));
    setConceptsInGroup(group);
  };

  const onMenuItemClick = (item) => {
    if (item.key === 'all') {
      setConceptsInGroup(allGroups);
    } else {
      onGroupItemClick(item.key);
    }
  };

  const handleModalOk = () => {
    form.validateFields().then((data) => {
      if (!files.length) {
        msgApi.error('please input the file');
        return;
      }
      runCreateNewCodeSystem(files[0]?.file, data.name, data.description ?? '', data.version);
    });
  };

  const handleModalCancel = () => {
    setIsModalOpen(false);
  };

  const onFileUpdate = (files) => {
    setFiles(files);
  };

  return (
    <div class="p-4">
      <div class="mb-4 flex justify-between items-center">
        <div>
          <h2>{codeSystemList?.data?.name}</h2>
          <h3 class="text-gray-400 inline mr-3">{codeSystemList?.data?.description}</h3>
        </div>
        <Space>
          {codeSystemList?.data?.version && (
            <Select
              defaultValue={codeSystemList?.data?.version}
              options={allVersionSelectOptions}
              onSelect={(version) => {
                runGetCodeSystemList(version);
              }}
              style={{ width: 120 }}
            />
          )}

          <Button type="primary" onClick={() => setIsModalOpen(true)} icon={<PlusOutlined />}>
            Code System
          </Button>
          <Button
            type="primary"
            loading={exportCodeSystemLoading}
            onClick={() => runExportCodeSystem(codeSystemList?.data?.version)}
            icon={<DownloadOutlined />}
          >
            Export
          </Button>
          <Popconfirm
            title="Delete the code system"
            description="Are you sure to delete this code system?"
            onConfirm={() => runDeleteCodeSystem(codeSystemList?.data?.version)}
            okText="Yes"
            cancelText="No"
          >
            <Button style={{ marginRight: '10px' }} loading={deleteCodeSystemLoading} danger>
              Delete
            </Button>
          </Popconfirm>
        </Space>
      </div>
      {getCodeSystemListLoading ? (
        <Spin />
      ) : (
        <Layout class="p-4">
          <div class="flex flex-col items-stretch" style={{ height: '80vh' }}>
            <div class="flex flex-col items-stretch overflow-scroll" style={{ flex: '0 auto' }}>
              <Sider width={250} breakpoint="sm" theme="light" style={{ background: '#fafafa' }}>
                <Menu
                  style={{ background: '#fafafa' }}
                  onClick={onMenuItemClick}
                  defaultSelectedKeys={['all']}
                  mode="inline"
                  items={sidebarItems}
                  theme="light"
                />
              </Sider>
            </div>
          </div>

          <Layout class="p-4 flex flex-col" style={{ height: '80vh' }}>
            <Content class="ml-3" style={{ flex: '1 1 auto', overflow: 'auto' }}>
              <CodeCard data={conceptsInGroup ?? []} />
            </Content>
          </Layout>
        </Layout>
      )}

      <Modal
        open={isModalOpen}
        onOk={handleModalOk}
        onCancel={handleModalCancel}
        okButtonProps={{ disabled: !files.length, loading: createNewCodeSystemLoading }}
        title="Create New Code System"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            label="Name"
            name="name"
            rules={[
              {
                required: true,
                message: 'Please input the name!',
              },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="version"
            name="version"
            rules={[
              {
                required: true,
                message: 'Please input the version!',
              },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item label="Description" name="description">
            <Input.TextArea />
          </Form.Item>
        </Form>
        <FileUploader files={files} onFileUpdate={onFileUpdate} />
      </Modal>
    </div>
  );
}
