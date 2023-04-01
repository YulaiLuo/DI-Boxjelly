import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { UserOutlined, DownOutlined } from '@ant-design/icons';
import { Layout, Menu, Avatar, Space, Dropdown } from 'antd';
import { removeTokens } from '../../utils/auth'

const { Sider, Header, Content } = Layout;

export default function Dashboard() {
  const navigate = useNavigate();
  const location = useLocation();
  let selectedPath = location.pathname.split('/').pop();
  if (selectedPath === '') selectedPath = 'mapping';

  const onMenuItemClick = (item) => {
    navigate(`/${item.key}`, {replace: true});
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
    console.log('sign out');
    removeTokens();
    navigate('/login', {replace: true})
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
          <Header class="bg-white px-8 py-3 flex">
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
            <Outlet />
          </Content>
        </Layout>
      </Layout>
    </>
  );
}
