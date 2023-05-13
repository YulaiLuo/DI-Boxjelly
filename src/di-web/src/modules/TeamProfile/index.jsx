import React from 'react';
import { List, Avatar, Layout, Menu } from 'antd';

const { Sider, Content } = Layout;

export default function TeamProfile() {
  const data = [
    {
      title: 'Vlada',
      description: 'vlada@unimelb.edu.au',
    },
    {
      title: 'Daniel',
      description: 'daniel@unimelb.edu.au',
    },
    {
      title: 'Mike',
      description: 'Mike@unimelb.edu.au',
    },
    {
      title: 'Mike',
      description: 'Mike@unimelb.edu.au',
    },
  ];

  const getSidebarItem = (label, key, icon, children) => ({
    label,
    key,
    children,
    icon,
  });

  const sidebarItems = [
    getSidebarItem('All members', 'all'),
    getSidebarItem('Pending', 'pending')
  ];

  return (
    <div class="mx-4 py-3">
      <div class="flex items-center">
        <h2 class="mr-5">You are currently in the XXXX team </h2>
        <a>Switch team</a>
      </div>

      <Layout>
        <Sider breakpoint="md" theme="light" style={{ background: '#fafafa' }}>
          <Menu
            style={{ background: '#fafafa' }}
            // onClick={onMenuItemClick}
            defaultSelectedKeys={['all']}
            // selectedKeys={[selectedPath]}
            mode="inline"
            items={sidebarItems}
            theme="light"
          />
        </Sider>

        <Layout>
          <Content class="ml-3">
            <List
              itemLayout="horizontal"
              dataSource={data}
              renderItem={(item, index) => (
                <List.Item actions={[<a key="remove">Remove</a>, <a key="leave">Leave</a>]}>
                  <List.Item.Meta
                    style={{ display: 'flex', alignItems: 'center' }}
                    avatar={
                      <Avatar
                        // class="mt-4"
                        src={`https://xsgames.co/randomusers/avatar.php?g=pixel&key=${index}`}
                      />
                      // <Avatar class="mt-4" src={`https://xsgames.co/randomusers/avatar.php?g=pixel&key=${index}`} />
                    }
                    title={item.title}
                    description={item.description}
                  />
                </List.Item>
              )}
            />
          </Content>
        </Layout>
      </Layout>
    </div>
  );
}
