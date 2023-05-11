import React, { useState } from 'react';
import { Collapse, Button, Layout, Menu } from 'antd';
import { useRequest } from 'ahooks';
import CodeCard from './components/CodeCard';
import { getCodeSystemList, getCodeSystemListByGroup } from './api';

const { Panel } = Collapse;
const { Sider, Content } = Layout;

export default function CodeSystem() {
  const [concepts, setConcepts] = useState([]);

  const { data: codeSystemList, run: runCodeSystemList } = useRequest(
    () => getCodeSystemList('1234', 'code_system_id'),
    {
      onSuccess: (data) => {
        console.log('data', data);
        setConcepts(() => {
          const concepts = data.data?.groups?.map((item) => item.concepts);
          return concepts.reduce((pre, cur) => [...pre, ...cur], []);
        });
      },
    }
  );

  const { loading, run: runCodeSystemListByGroup } = useRequest(getCodeSystemListByGroup, {
    manual: true,
    onSuccess: (result) => {
      console.log('restult', result);
      setConcepts(result.data?.concepts);
    },
  });

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
        label: group.group,
        key: group.group_id,
      };
    }),
  ];

  const onMenuItemClick = (item) => {
    console.log(item);
    if (item.key === 'all') {
      runCodeSystemList('1234', 'code_system_id');
    } else {
      runCodeSystemListByGroup(item.key);
    }
  };

  return (
    <div class="p-4">
      <div class="mb-4 flex justify-between items-center">
        <h2>{codeSystemList?.data?.description}</h2>
        <Button type="primary">Add a new group</Button>
      </div>
      <Layout>
        <Sider breakpoint="md" theme="light" style={{ background: '#fafafa' }}>
          <Menu
            style={{ background: '#fafafa' }}
            onClick={onMenuItemClick}
            defaultSelectedKeys={['all']}
            // selectedKeys={[selectedPath]}
            mode="inline"
            items={sidebarItems}
            theme="light"
          />
        </Sider>

        <Layout>
          <Content class="ml-3">
            <CodeCard data={concepts ?? []} />
          </Content>
        </Layout>
      </Layout>
      {/* <div>
        <Collapse>
          {groups.map((item, i) => {
            return (
              <Panel header={group} key={i}>
                <CodeCard data={data ?? []} />
              </Panel>
            );
          })}
        </Collapse>
       
      </div> */}
    </div>
  );
}
