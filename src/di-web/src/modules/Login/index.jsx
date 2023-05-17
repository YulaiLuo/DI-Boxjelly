import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useRequest } from 'ahooks';
import { Form, Input, Button } from 'antd';
import { login } from './api';
import { useMessageStore, useUserStore } from '../../store';
import Cookies from 'js-cookie';

export default function Login() {
  const navigate = useNavigate();
  const msgApi = useMessageStore((state) => state.msgApi);
  const setLoggedIn = useUserStore((state) => state.setLoggedIn);

  const { loading, run } = useRequest(login, {
    manual: true,
    onSuccess: (res) => {
      console.log('login', res);
      localStorage.setItem('user', res.data?.user?.id);
      localStorage.setItem('team', res.data?.team?.id);
      localStorage.setItem('userDetail', JSON.stringify(res.data?.user));
      setLoggedIn(true);
      // const cookies = document.cookie.split(';');
      // console.log('cookies', cookies);
      const csrfCookie = Cookies.get('csrf_access_token');
      console.log('csrf', csrfCookie);
      msgApi.success('Login Successfully');
      localStorage.setItem('loggedIn', 'true');
      navigate('/dashboard', { replace: true });
    },
  });

  return (
    <div class="h-screen flex justify-center items-center">
      <div class="w-96">
        <h1 class="mb-6 text-center text-primary">Mapping</h1>
        <Form onFinish={(data) => run(data)} layout="vertical">
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
              <Button type="primary" htmlType="submit" loading={loading} block>
                Login
              </Button>
            </div>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
}
