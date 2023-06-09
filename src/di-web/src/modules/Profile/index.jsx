// Import necessary modules and components
import React, { useState } from 'react';
import { useRequest } from 'ahooks';
import { getUserProfile, updateUserProfile } from './api';
import {
  Avatar,
  Button,
  Form,
  Input,
  Select,
  Space,
  Upload,
  Row,
  Col,
  Card,
  notification,
} from 'antd';
import {
  UserOutlined,
  SmileOutlined,
  MailOutlined,
  EditOutlined,
  ManOutlined,
  WomanOutlined,
  QuestionOutlined,
  UploadOutlined,
} from '@ant-design/icons';
import { BASE_URL } from '../../utils/constant/url';
import { getCSRFTokenHeader } from '../../utils/auth';
import { useUserStore } from '../../store';

// Define the Option component for Select field
const { Option } = Select;

// Main UserProfile component
const UserProfile = () => {
  // Use global state management to share user data across components
  const userData = useUserStore((state) => state.user);
  const setUserData = useUserStore((state) => state.setUser);

  // Retrieve user_id from local storage
  const user_id = localStorage.getItem('user');

  // Define states for edit mode and form controls
  const [editMode, setEditMode] = useState(false);
  const [form] = Form.useForm();

  // Define a request to get user profile
  const { run: runGetUserProfile } = useRequest(() => getUserProfile(user_id), {
    onSuccess: (response) => {
      // Process and store user profile details on successful fetch
      const [first_name, last_name] = response.data.name.split(' ');
      const userDetails = {
        email: response.data.email,
        first_name,
        last_name,
        nickname: response.data.nickname,
        gender: response.data.gender || '',
        avatar: response.data.avatar || '', // Store avatar
      };

      // Set user data in global state and local storage
      setUserData(userDetails);
      localStorage.setItem('userDetail', JSON.stringify(userDetails));
    },
  });

  // Define a request to update user profile
  const { run: runUpdateUserProfile, loading: updateUserProfileLoading } = useRequest(
    updateUserProfile,
    {
      manual: true,
      onSuccess: () => {
        // After successful update, turn off edit mode and refresh user profile data
        setEditMode(false);
        runGetUserProfile(user_id);
        notification.success({
          message: 'Success',
          description: 'Profile updated successfully!',
          duration: 3,
        });
      },
    }
  );

  // Define handler for saving changes to user profile
  const handleSaveChanges = (values) => {
    runUpdateUserProfile(user_id, {
      first_name: values.first_name,
      last_name: values.last_name,
      nickname: values.nickname,
      gender: values.gender,
    });
  };

  // Render UserProfile component
  return (
    <div style={{ padding: '1rem' }}>
      <Row justify="center" align="middle" style={{ minHeight: '90vh' }}>
        <Col xs={24} sm={22} md={20} lg={12} xl={8}>
          <Card style={{ width: '100%', textAlign: 'center' }}>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              {editMode ? (
                <Form
                  form={form}
                  layout="vertical"
                  onFinish={handleSaveChanges}
                  initialValues={userData}
                >
                  <Avatar
                    size={128}
                    src={`${BASE_URL}/auth/user/avatar?avatar=${userData.avatar}`}
                  />
                  <Form.Item>
                    <Upload
                      action={`${BASE_URL}/auth/user/avatar`}
                      headers={getCSRFTokenHeader()}
                      withCredentials={true}
                    >
                      <Button icon={<UploadOutlined />}>Change Avatar</Button>
                    </Upload>
                  </Form.Item>
                  <Form.Item label="First name" name="first_name">
                    <Input />
                  </Form.Item>
                  <Form.Item label="Last name" name="last_name">
                    <Input />
                  </Form.Item>
                  <Form.Item label="Nickname" name="nickname">
                    <Input />
                  </Form.Item>
                  <Form.Item label="Email" name="email">
                    <Input disabled />
                  </Form.Item>
                  <Form.Item label="Gender" name="gender">
                    <Select>
                      <Option value="Male">Male</Option>
                      <Option value="Female">Female</Option>
                      <Option value="Other">Other</Option>
                    </Select>
                  </Form.Item>
                  <Form.Item>
                    <Button type="primary" htmlType="submit" loading={updateUserProfileLoading}>
                      Save Changes
                    </Button>
                  </Form.Item>
                </Form>
              ) : (
                <div>
                  <Avatar
                    size={128}
                    src={`${BASE_URL}/auth/user/avatar?avatar=${userData.avatar}`}
                  />
                  <p>
                    <UserOutlined /> <strong>Name:</strong>{' '}
                    {`${userData.first_name} ${userData.last_name}`}
                  </p>
                  <p>
                    <SmileOutlined /> <strong>Nickname:</strong> {userData.nickname}
                  </p>
                  <p>
                    <MailOutlined /> <strong>Email:</strong> {userData.email}
                  </p>
                  <p>
                    {userData.gender === 'Male' ? (
                      <ManOutlined />
                    ) : userData.gender === 'Female' ? (
                      <WomanOutlined />
                    ) : (
                      <QuestionOutlined />
                    )}{' '}
                    <strong>Gender:</strong> {userData.gender}
                  </p>
                  <Button type="primary" icon={<EditOutlined />} onClick={() => setEditMode(true)}>
                    Edit Profile
                  </Button>
                </div>
              )}
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

// Export UserProfile component
export default UserProfile;
