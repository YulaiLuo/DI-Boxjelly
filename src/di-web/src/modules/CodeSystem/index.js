import React, { useState, useRef, useEffect } from 'react';
import { Button, Layout, Menu, Modal, Input, Dropdown, Space, Tooltip } from 'antd';
import { MoreOutlined } from '@ant-design/icons';
import { useRequest } from 'ahooks';
import CodeCard from './components/CodeCard';
import { getAllConcepts, getCodeSystemList, getCodeSystemListByGroup } from './api';
import { Spin } from '../../components';

const { Sider, Content } = Layout;

export default function CodeSystem() {
  const newGroupInputRef = useRef();

  const [concepts, setConcepts] = useState([]);
  const [newGroupName, setNewGroupName] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const { data: codeSystemList } = useRequest(
    () => getCodeSystemList('60c879e72cb0e6f96d6b0f65', '645a4f69203d1d8b3fbb80b4'),
    {
      initialData: [],
    }
  );

  const { loading: conceptsLoading, run: runCodeSystemListByGroup } = useRequest(
    getCodeSystemListByGroup,
    {
      manual: true,
      onSuccess: (result) => {
        setConcepts(result.data?.concepts);
      },
    }
  );

  const { loading: allConceptsLoading, run: runCodeSystemList } = useRequest(getAllConcepts, {
    manual: true,
    onSuccess: (result) => {
      setConcepts(result.data?.concepts);
    },
  });

  useEffect(() => {
    runCodeSystemList('645a4f69203d1d8b3fbb80b4');
  }, []); // Add this useEffect hook

  console.log(codeSystemList);

  const groups = codeSystemList?.data?.groups ?? [];

  // const data = codeSystemList?.data?.groups[0].concepts;
  // const group = codeSystemList?.data?.groups[0].group;

  const sidebarItems = [
    {
      label: 'All',
      key: 'all',
    },
    ...groups.map((group) => {
      return {
        label: (
          <div class="flex justify-between">
            <Tooltip title={group.group}>
              <span className="overflow-hidden overflow-ellipsis">{group.group}</span>
            </Tooltip>
          </div>
        ),
        key: group.group_id,
      };
    }),
  ];

  const onMenuItemClick = (item) => {
    console.log(item);
    if (item.key === 'all') {
      runCodeSystemList('645a4f69203d1d8b3fbb80b4');
    } else {
      runCodeSystemListByGroup(item.key);
    }
  };

  const handleModalOk = () => {
    setIsModalOpen(false);
  };

  const handleModalCancel = () => {
    setIsModalOpen(false);
  };

  return (
    <div class="p-4">
      <div class="mb-4 flex justify-between items-center" style={{ flex: '0 0 66.6%' }}>
        <div>
          <h2 class="inline mr-4">{codeSystemList?.data?.name}</h2>
          <h3 class="text-gray-400">{codeSystemList?.data?.description}</h3>
        </div>
        <Space>
          <Button type="primary" style={{ marginRight: '10px' }}>
            Update UIL
          </Button>
        </Space>
      </div>
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
            {conceptsLoading || allConceptsLoading ? <Spin /> : <CodeCard data={concepts ?? []} />}
          </Content>
        </Layout>
      </Layout>

      <Modal open={isModalOpen} onOk={handleModalOk} onCancel={handleModalCancel}>
        <Input placeholder="UIL" />
      </Modal>
    </div>
  );
}
