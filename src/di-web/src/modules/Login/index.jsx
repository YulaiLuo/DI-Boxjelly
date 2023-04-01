import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button } from 'antd';
import { login } from './api';
import { useMessageStore } from '../../store';
import { setTokens } from '../../utils/auth';

export default function Login() {
  const navigate = useNavigate();
  const msgApi = useMessageStore((state) => state.msgApi);

  console.log('login', msgApi);

  const onFinish = async (data) => {
    login(data).then((res) => {
      setTokens();
      msgApi.success('Login Successfully');
      navigate('/mapping', { replace: true });
    });
  };

  return (
    <div class="h-screen flex justify-center items-center">
      <div class="w-96">
        <h1 class="mb-6 text-center text-primary">Mapping</h1>
        <Form onFinish={onFinish} layout="vertical">
          <Form.Item
            label="Email"
            name="email"
            rules={[{ required: true, message: 'Please input your email!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: 'Please input your password!' }]}
          >
            <Input.Password />
          </Form.Item>
          <Form.Item>
            <div class="mt-3">
              <Button type="primary" htmlType="submit" block>
                Login
              </Button>
            </div>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
}
