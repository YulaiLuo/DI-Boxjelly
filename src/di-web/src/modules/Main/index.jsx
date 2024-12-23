// This file defines the Main component of the application, 
// which is the component responsible for rendering the main layout and the dashboard.
import React, { useState } from 'react';
// Importing required dependencies and components
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
import { useUserStore, useMessageStore } from '../../store';
import { getBoardList, editBoard, createBoard, deleteBoard, logout } from './api';
import { BASE_URL } from '../../utils/constant/url';

// Layout constants
const { Sider, Header, Content } = Layout;
const { PUBLIC_URL } = process.env;

// The Main component
export default function Main() {
  // State variables and hooks used for various functionalities in the component
  // These include flags for modals, form objects, and data from user store and message store
  // Also includes API calls with ahooks' useRequest, to interact with backend
  const [collapsed, setCollapsed] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [boardId, setBoardId] = useState(null);
  const user = useUserStore((state) => state.user);
  const msgApi = useMessageStore((state) => state.msgApi);

  const [createBoardForm] = Form.useForm();
  const [editBoardForm] = Form.useForm();

  const navigate = useNavigate();
  const location = useLocation();
  const teamId = localStorage.getItem('team');
  // const user = JSON.parse(localStorage.getItem('userDetail'));
  let selectedPath = location.pathname;
  if (selectedPath === '') selectedPath = 'dashboard';

  const { data, refresh: refreshBoardList } = useRequest(() => getBoardList(teamId));
  const taskBoards = data?.data?.boards ?? [];

  const { run: runCreateBoard, loading: createBoardLoading } = useRequest(createBoard, {
    manual: true,
    onSuccess: () => {
      msgApi.success('A new board created successfully');
      setIsModalOpen(false);
      createBoardForm.resetFields();
      refreshBoardList(teamId);
    },
  });

  const { run: runEditBoard, loading: editBoardLoading } = useRequest(editBoard, {
    manual: true,
    onSuccess: () => {
      msgApi.success('The board is updated successfully');
      setIsEditModalOpen(false);
      editBoardForm.resetFields();
      refreshBoardList(teamId);
      setTimeout(() => {
        window.location.reload();
      }, 500);
    },
  });

  const { run: runDeleteBoard } = useRequest(deleteBoard, {
    manual: true,
    onSuccess: () => {
      msgApi.success('The board is deleted successfully');
      navigate('/dashboard', { replace: true });
      refreshBoardList(teamId);
    },
  });

  const { run: runLogout } = useRequest(logout, {
    manual: true,
    onSuccess: () => {
      // removeTokens();
      navigate('/login', { replace: true });
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

  const onBoardEditClick = (board) => {
    editBoardForm.setFieldsValue({
      name: board.name,
      description: board.description,
    });
    setIsEditModalOpen(true);
  };

  const onBoardDeleteClick = (board) => {
    runDeleteBoard(board.id, teamId);
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
              { key: 'edit', label: 'Edit' },
              { key: 'delete', label: 'Delete' },
            ],
            onClick: (e) => {
              if (e.key === 'edit') {
                setBoardId(board.id);
                onBoardEditClick(board);
              } else {
                onBoardDeleteClick(board);
              }
            },
          }}
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
    getSidebarItem(getBoardListTitle(), '/mapping-history', null, 'group', taskBoardItems),
  ];

  const collapsedSidebarItems = [
    getSidebarItem('Dashboard', '/dashboard', <HomeOutlined />),
    getSidebarItem(getMemberItem(), '/team-profile', <UserOutlined />),
    getSidebarItem('Code System', '/code-system', <InsertRowAboveOutlined />),
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

  const onProfileClick = () => {
    navigate('/profile');
  };

  const onDropdownItemClick = (e) => {
    if (e.key === 'profile') onProfileClick();
    else if (e.key === 'signOut') runLogout();
  };

  const handleCreateBoardModalOk = () => {
    createBoardForm.validateFields().then((data) => {
      const boardName = data.name;
      const description = data.description ?? '';
      runCreateBoard(teamId, boardName, description);
    });
  };

  const handleEditBoardModalOk = () => {
    editBoardForm.validateFields().then((data) => {
      const boardName = data.name;
      const description = data.description ?? '';
      runEditBoard(boardId, teamId, boardName, description);
    });
  };

  // Implementing the main return function
  return (
    <>
      <Layout hasSider>
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={(value) => setCollapsed(value)}
          breakpoint="md"
          style={{ position: 'fixed', height: '100vh', overflow: 'auto' }}
          theme="light"
        >
          <div class="m-4 flex items-center justify-center">
            <img src={`${PUBLIC_URL}/logo512.png`} alt="" width={30} />
            {!collapsed && <span class="font-bold text-primary ml-2 text-xl">Mapping</span>}
          </div>
          <Menu
            onClick={onMenuItemClick}
            defaultSelectedKeys={[selectedPath]}
            selectedKeys={[selectedPath]}
            mode="inline"
            items={collapsed ? collapsedSidebarItems : sidebarItems}
            theme="light"
          />
        </Sider>

        <Layout style={{ marginLeft: collapsed ? 80 : 200 }}>
          <Header class="bg-white px-8 py-3 flex sticky top-0 z-10 w-full">
            <Space class="flex-1 flex justify-end items-center" size={12}>
              <Avatar
                icon={<UserOutlined />}
                size="large"
                src={`${BASE_URL}/auth/user/avatar?avatar=${user?.avatar}`}
              />

              <Dropdown menu={{ items: ProfileDropdownItems, onClick: onDropdownItemClick }}>
                <div>
                  <span class="text-lg cursor-pointer mr-2">{user?.nickname}</span>
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
        onOk={handleCreateBoardModalOk}
        onCancel={() => setIsModalOpen(false)}
        confirmLoading={createBoardLoading}
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
      </Modal>

      <Modal
        title="Edit the Board"
        open={isEditModalOpen}
        onOk={handleEditBoardModalOk}
        onCancel={() => setIsEditModalOpen(false)}
        confirmLoading={editBoardLoading}
      >
        <Form form={editBoardForm} layout="vertical">
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
      </Modal>
    </>
  );
}
