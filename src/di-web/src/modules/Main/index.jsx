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
import { useUserStore, useMessageStore } from '../../store';
import { getBoardList, editBoard, createBoard, deleteBoard } from './api';

const { Sider, Header, Content } = Layout;
const { PUBLIC_URL } = process.env;

export default function Main() {
  const [collapsed, setCollapsed] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [boardId, setBoardId] = useState(null);
  const setLoggedIn = useUserStore((state) => state.setLoggedIn);
  const msgApi = useMessageStore((state) => state.msgApi);

  const [createBoardForm] = Form.useForm();
  const [editBoardForm] = Form.useForm();

  const navigate = useNavigate();
  const location = useLocation();
  const teamId = localStorage.getItem('team');
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
      msgApi.success('A new board created successfully');
      setIsEditModalOpen(false);
      editBoardForm.resetFields();
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

  const onBoardEditClick = (board) => {
    console.log('edit', board);
    editBoardForm.setFieldsValue({
      name: board.name,
      description: board.description,
    });
    setIsEditModalOpen(true);
  };

  const onBoardDeleteClick = (board) => {
    console.log('delete', board);
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
