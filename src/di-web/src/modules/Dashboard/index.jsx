import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';

const { Sider, Header, Content } = Layout;

export default function Dashboard() {
  const navigate = useNavigate();
  const location = useLocation();
  let selectedPath = location.pathname.split('/').pop();
  if (selectedPath === '')
    selectedPath = 'mapping'

  const onMenuItemClick = (item) => {
    navigate(`/${item.key}`);
  };

  const getSidebarItem = (label, key, children, icon) => ({
    label,
    key,
    children,
    icon,
  });

  const sidebarItems = [
    getSidebarItem('Main', 'mapping'),
    getSidebarItem('History Status', 'history', [
      getSidebarItem('Retrain History', 'retrain-history'),
      getSidebarItem('Mapping History', 'mapping-history'),
    ]),
    getSidebarItem('Account', 'profile'),
  ];

  return (
    <>
      <Layout style={{ height: '100vh' }}>
        <Sider>
          <Menu
            style={{ height: '100%' }}
            onClick={onMenuItemClick}
            defaultSelectedKeys={[selectedPath]}
            mode="inline"
            items={sidebarItems}
          />
        </Sider>
        <Layout>
          <Header style={{ background: 'white' }}>
            <div>Header</div>
          </Header>
          <Content>
            <Outlet />
          </Content>
        </Layout>
      </Layout>
    </>
  );
}
