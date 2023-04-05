import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { UserOutlined, DownOutlined, HomeOutlined, PieChartOutlined } from '@ant-design/icons';
import { Layout, Menu, Avatar, Space, Dropdown } from 'antd';
import { useUserStore } from '../../store';

const { Sider, Header, Content } = Layout;

export default function Dashboard() {
  const [collapsed, setCollapsed] = useState(false);
  const setLoggedIn = useUserStore((state) => state.setLoggedIn)

  const navigate = useNavigate();
  const location = useLocation();
  let selectedPath = location.pathname.split('/').pop();
  if (selectedPath === '') selectedPath = 'mapping';

  const onMenuItemClick = (item) => {
    navigate(`/${item.key}`, { replace: true });
  };

  const getSidebarItem = (label, key, icon, children) => ({
    label,
    key,
    children,
    icon,
  });

  const sidebarItems = [
    getSidebarItem('Main', 'mapping', <HomeOutlined />),
    getSidebarItem('History Status', 'history', <PieChartOutlined />, [
      getSidebarItem('Retrain History', 'retrain-history'),
      getSidebarItem('Mapping History', 'mapping-history'),
    ]),
    getSidebarItem('Account', 'profile', <UserOutlined />),
  ];

  const ProfileDropdownItems = [
    {
      key: 'profile',
      label: 'Your Profile',
    },
    {
      key: 'signOut',
      label: 'Sign out',
    },
  ];

  const onSignOutClick = () => {
    setLoggedIn(false);
    navigate('/login', { replace: true });
  };

  const onProfileClick = () => {
    console.log('go to profile page');
  };

  const onDropdownItemClick = (e) => {
    if (e.key === 'profile') onProfileClick();
    else if (e.key === 'signOut') onSignOutClick();
  };

  return (
    <>
      <Layout style={{ height: '100vh' }}>
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={(value) => setCollapsed(value)}
          theme="light"
        >
          <div class="m-4 text-center text-2xl font-bold text-primary">
            {collapsed ? 'M' : 'Mapping'}
          </div>
          <Menu
            style={{ height: '100vh' }}
            onClick={onMenuItemClick}
            defaultSelectedKeys={[selectedPath]}
            mode="inline"
            items={sidebarItems}
            theme="light"
          />
        </Sider>
        <Layout>
          <Header class="bg-white px-8 py-3 flex sticky top-0 z-10 w-full">
            {/* <span class="self-center">Header</span> */}

            <Space class="flex-1 flex justify-end items-center" size={12}>
              <Avatar icon={<UserOutlined />} size="large" />

              <Dropdown menu={{ items: ProfileDropdownItems, onClick: onDropdownItemClick }}>
                <div>
                  <span class="text-lg cursor-pointer mr-2">Daniel</span>
                  <DownOutlined />
                </div>
              </Dropdown>
            </Space>
          </Header>
          <Content>
            <div class="bg-[#fafafa] h-full">
              <Outlet />
            </div>
          </Content>
        </Layout>
      </Layout>
    </>
  );
}
