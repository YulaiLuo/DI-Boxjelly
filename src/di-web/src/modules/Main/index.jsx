import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  UserOutlined,
  DownOutlined,
  HomeOutlined,
  PlusOutlined,
  InsertRowAboveOutlined,
  MoreOutlined,
} from '@ant-design/icons';
import { Layout, Menu, Avatar, Space, Dropdown, Tooltip, Modal, Input, Form } from 'antd';
import { useRequest } from 'ahooks';
import { useUserStore } from '../../store';
import { getBoardList, editBoard, createBoard, deleteBoard } from './api';

const { Sider, Header, Content } = Layout;
const { PUBLIC_URL } = process.env;

export default function Main() {
  const [collapsed, setCollapsed] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newBoardName, setNewBoardName] = useState('');
  const setLoggedIn = useUserStore((state) => state.setLoggedIn);

  const [createBoardForm] = Form.useForm();

  const navigate = useNavigate();
  const location = useLocation();
  const teamId = localStorage.getItem('team');
  console.log('path', location.pathname);
  let selectedPath = location.pathname;
  if (selectedPath === '') selectedPath = 'dashboard';

  const { data, refresh: refreshBoardList } = useRequest(() => getBoardList(teamId));
  const taskBoards = data?.data?.boards ?? [];

  const { run: runCreateBoard } = useRequest(createBoard, {
    manual: true,
    onSuccess: () => {
      setIsModalOpen(false);
      setNewBoardName('');
      refreshBoardList(teamId);
    },
  });

  const onMenuItemClick = (item) => {
    navigate(`${item.key}`, { replace: true });
  };

  const getSidebarItem = (label, key, icon, type, children) => ({
    label,
    key,
    children,
    icon,
    type,
  });

  const getMemberItem = () => {
    return (
      <div class="flex justify-between">
        <span>Members</span>
      </div>
    );
  };

  const onBoarListDropdownItemClick = () => {
    console.log('first');
  };

  const taskBoardItems = taskBoards.map((board) => {
    return getSidebarItem(
      <div class="flex justify-between">
        <Tooltip title={board.name}>
          <span className="overflow-hidden overflow-ellipsis">{board.name}</span>
        </Tooltip>

        <Dropdown
          menu={{
            items: [
              { key: 'edit', label: 'edit' },
              { key: 'delete', label: 'delete' },
            ],
            onClick: onBoarListDropdownItemClick,
          }}
          // open={true}
        >
          <MoreOutlined>dfd</MoreOutlined>
        </Dropdown>
      </div>,
      `/mapping-history/${board.id}`
    );
  });

  const getBoardListTitle = () => {
    return (
      <div class="flex justify-between">
        <span>Boards</span>
        <PlusOutlined class="cursor-pointer" onClick={() => setIsModalOpen(true)} />
      </div>
    );
  };

  const sidebarItems = [
    getSidebarItem('Dashboard', '/dashboard', <HomeOutlined />),
    getSidebarItem(getMemberItem(), '/team-profile', <UserOutlined />),
    getSidebarItem('Code System', '/code-system', <InsertRowAboveOutlined />),
    // getSidebarItem('Mapping', 'mapping', <HomeOutlined />),
    // getSidebarItem('Task Board', 'mapping-history', <PieChartOutlined />),
    // getSidebarItem('History Status', 'history', <PieChartOutlined />, [
    //   getSidebarItem('Retrain History', 'retrain-history'),
    //   getSidebarItem('Mapping History', 'mapping-history'),
    // ]),
    getSidebarItem(getBoardListTitle(), '/mapping-history', null, 'group', taskBoardItems),
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
    navigate('/profile');
  };

  const onDropdownItemClick = (e) => {
    if (e.key === 'profile') onProfileClick();
    else if (e.key === 'signOut') onSignOutClick();
  };

  const handleModalOk = () => {
    console.log(newBoardName);
    createBoardForm.validateFields().then((data) => {
      const boardName = data.name;
      const description = data.description ?? '';

      runCreateBoard(teamId, boardName, description);
    });
  };

  const handleModalCancel = () => {
    setIsModalOpen(false);
    setNewBoardName('');
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
                  <span class="text-lg cursor-pointer mr-2">User</span>
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
      <Modal
        title="Add a new Board"
        open={isModalOpen}
        onOk={handleModalOk}
        onCancel={handleModalCancel}
      >
        <Form form={createBoardForm} layout="vertical">
          <Form.Item
            label="Board Name"
            name="name"
            rules={[
              {
                required: true,
                message: 'Please input the board name!',
              },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item label="Description" name="description">
            <Input.TextArea />
          </Form.Item>
        </Form>
        {/* <Input
          placeholder="please input the board name"
          onChange={(e) => setNewBoardName(e.target.value)}
          value={newBoardName}
        />
        <Input.TextArea /> */}
      </Modal>
    </>
  );
}
