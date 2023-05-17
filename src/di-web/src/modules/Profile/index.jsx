import React, { useEffect, useState } from "react";
import { getUserProfile, updateUserProfile } from './api';
import { Avatar, Button, Form, Input, Select, Space, Typography, Upload } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { BASE_URL } from '../../utils/constant/url';

const { Title } = Typography;
const { Option } = Select;

const UserProfile = () => {
  const [userData, setUserData] = useState({
    email: "",
    first_name: "",
    last_name: "",
    nickname: "",
    gender: "",
    avatar: ""
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
        gender: response.data.gender || "Not specified",
        avatar: response.data.avatar || "Not specified" // Store avatar 
      };

      setUserData(userDetails);

      // store the user detail in local storage
      localStorage.setItem('userDetail', JSON.stringify(userDetails));
      
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
        //replace it with a better solution: let the dashboard detect the change and then update its details dynamically
        // window.location.reload();
      } else {
        console.log(response.msg);
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div style={{ 
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh', 
      padding: '1rem' 
    }}>
      <div style={{ maxWidth: '400px', width: '100%', textAlign: 'center' }}>
        <Title>User Profile</Title>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <Avatar size={128} src={`${BASE_URL}/auth/user/avatar?avatar=${userData.avatar}`}/>
        {editMode ? (
          <Form form={form} layout="vertical" >
            <Form.Item label="First name" >
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
                onChange={(e) =>
                  setUserData({ ...userData, nickname: e.target.value })
                }
              />
            </Form.Item>
            <Form.Item label="Email">
              <Input
                value={userData.email}
                readOnly
              />
            </Form.Item>
            <Form.Item label="Gender">
              <Select
                value={userData.gender}
                onChange={(value) =>
                  setUserData({ ...userData, gender: value })
                }
              >
                <Option value="male">Male</Option>
                <Option value="female">Female</Option>
                <Option value="other">Other</Option>
              </Select>
            </Form.Item>
            <Form.Item label="Avatar">
              <Upload action={`${BASE_URL}/auth/user/avatar`}>
                <Button icon={<UploadOutlined />}>Click to Upload</Button>
              </Upload>
            </Form.Item>
            <Form.Item>
              <Button type="primary" onClick={handleSaveChanges}>Save Changes</Button>
            </Form.Item>
          </Form>
        ) : (
          <Space direction="vertical" style={{ width: '100%', textAlign: 'center' }}>
            <p><strong>Name:</strong> {`${userData.first_name} ${userData.last_name}`}</p>
            <p><strong>Nickname:</strong> {userData.nickname}</p>
            <p><strong>Email:</strong> {userData.email}</p>
            <p><strong>Gender:</strong> {userData.gender}</p>
            <Button type="primary" onClick={() => setEditMode(true)}>Edit Profile</Button>
          </Space>
        )}
      </Space>
    </div>
  </div>
  );
};

export default UserProfile;