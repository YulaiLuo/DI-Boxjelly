import React, { useEffect, useState } from 'react';
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
} from '@ant-design/icons';
import { UploadOutlined } from '@ant-design/icons';
import { BASE_URL } from '../../utils/constant/url';
import { getCSRFTokenHeader } from '../../utils/auth';

const { Option } = Select;

const UserProfile = () => {
  const [userData, setUserData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    nickname: '',
    gender: '',
    avatar: '',
  });
  const [editMode, setEditMode] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const user_id = localStorage.getItem('user');
      const response = await getUserProfile(user_id);
      const [first_name, last_name] = response.data.name.split(' ');

      const userDetails = {
        email: response.data.email,
        first_name,
        last_name,
        nickname: response.data.nickname,
        gender: response.data.gender || 'Not specified',
        avatar: response.data.avatar || 'Not specified', // Store avatar
      };

      setUserData(userDetails);

      // store the user detail in local storage
      localStorage.setItem('userDetails', JSON.stringify(userDetails));
    } catch (error) {
      console.log(error);
    }
  };

  const handleSaveChanges = async () => {
    const user_id = localStorage.getItem('user');

    try {
      const response = await updateUserProfile(user_id, {
        first_name: userData.first_name,
        last_name: userData.last_name,
        nickname: userData.nickname,
        gender: userData.gender,
      });

      if (response.code === 200) {
        setEditMode(false);
        fetchData();
        notification.success({
          message: 'Success',
          description: 'Profile updated successfully!',
          duration: 3,
        });
      } else {
        notification.error({
          message: 'Error',
          description: response.msg,
          duration: 3,
        });
      }
    } catch (error) {
      notification.error({
        message: 'Error',
        description: 'There was a problem updating your profile',
        duration: 3,
      });
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <Row justify="center" align="middle" style={{ minHeight: '90vh' }}>
        <Col xs={24} sm={22} md={20} lg={12} xl={8}>
          <Card style={{ width: '100%', textAlign: 'center' }}>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              {editMode ? (
                <Form form={form} layout="vertical">
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
                  <Form.Item label="First name">
                    <Input
                      value={userData.first_name}
                      onChange={(e) => setUserData({ ...userData, first_name: e.target.value })}
                    />
                  </Form.Item>
                  <Form.Item label="Last name">
                    <Input
                      value={userData.last_name}
                      onChange={(e) => setUserData({ ...userData, last_name: e.target.value })}
                    />
                  </Form.Item>
                  <Form.Item label="Nickname">
                    <Input
                      value={userData.nickname}
                      onChange={(e) => setUserData({ ...userData, nickname: e.target.value })}
                    />
                  </Form.Item>
                  <Form.Item label="Email">
                    <Input value={userData.email} readOnly />
                  </Form.Item>
                  <Form.Item label="Gender">
                    <Select
                      value={userData.gender}
                      onChange={(value) => setUserData({ ...userData, gender: value })}
                    >
                      <Option value="Male">Male</Option>
                      <Option value="Female">Female</Option>
                      <Option value="Other">Other</Option>
                    </Select>
                  </Form.Item>
                  <Form.Item>
                    <Button type="primary" onClick={handleSaveChanges}>
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

export default UserProfile;
