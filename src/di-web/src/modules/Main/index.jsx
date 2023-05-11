import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  UserOutlined,
  DownOutlined,
  HomeOutlined,
  PieChartOutlined,
  PlusOutlined,
} from '@ant-design/icons';
import { Layout, Menu, Avatar, Space, Dropdown } from 'antd';
import { useUserStore } from '../../store';

const { Sider, Header, Content } = Layout;
const { PUBLIC_URL } = process.env;

export default function Main() {
  const [collapsed, setCollapsed] = useState(false);
  const setLoggedIn = useUserStore((state) => state.setLoggedIn);

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

  const getMemberItem = () => {
    return (
      <div class="flex justify-between">
        <span>Members</span>
        <span>
          <PlusOutlined />
        </span>
      </div>
    );
  };

  const sidebarItems = [
    getSidebarItem('Dashboard', 'dashboard', <HomeOutlined />),
    getSidebarItem(getMemberItem(), 'profile', <UserOutlined />),
    getSidebarItem('Code System', 'code-system', <HomeOutlined />),
    // getSidebarItem('Mapping', 'mapping', <HomeOutlined />),
    getSidebarItem('Mapping History', 'mapping-history', <PieChartOutlined />),
    // getSidebarItem('History Status', 'history', <PieChartOutlined />, [
    //   getSidebarItem('Retrain History', 'retrain-history'),
    //   getSidebarItem('Mapping History', 'mapping-history'),
    // ]),
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
      <Layout hasSider>
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={(value) => setCollapsed(value)}
          breakpoint="md"
          style={{ position: 'fixed' }}
          theme="light"
        >
          <div class="m-4 flex items-center justify-center">
            <img src={`${PUBLIC_URL}/logo512.png`} alt="" width={30} />
            {!collapsed && <span class="font-bold text-primary ml-2 text-xl">Mapping</span>}
          </div>
          <Menu
            style={{ height: '100vh' }}
            onClick={onMenuItemClick}
            defaultSelectedKeys={[selectedPath]}
            selectedKeys={[selectedPath]}
            mode="inline"
            items={sidebarItems}
            theme="light"
          />
        </Sider>
        <Layout style={{ marginLeft: collapsed ? 80 : 200 }}>
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
