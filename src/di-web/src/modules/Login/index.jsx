/**
 * This file defines the Login component which is responsible for handling user logins.
 * It uses react hooks and the useRequest hook from ahooks library for making the API call.
 * The 'login' function for the API call is imported from the api.js file in the same module.
 * On successful login, user information is stored in local storage and state, and the user is redirected to the dashboard.
 */

// Importing required modules
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useRequest } from 'ahooks';
import { Form, Input, Button } from 'antd';
import { login } from './api';
import { useMessageStore, useUserStore } from '../../store';

/**
 * Login is a functional component for handling user logins.
 * It renders a form with fields for email and password, and a button for submitting the form.
 * On form submission, it calls the 'login' function to make the API request.
 * If the request is successful, it stores user information in local storage and state, displays a success message,
 * and navigates to the dashboard.
 */
export default function Login() {
  const navigate = useNavigate();
  const msgApi = useMessageStore((state) => state.msgApi);
  const setLoggedIn = useUserStore((state) => state.setLoggedIn);
  const setUserData = useUserStore((state) => state.setUser);

  const { loading, run } = useRequest(login, {
    manual: true,
    onSuccess: (res) => {
      localStorage.setItem('user', res.data?.user?.id);
      localStorage.setItem('team', res.data?.team?.id);
      localStorage.setItem('userDetail', JSON.stringify(res.data?.user));
      setUserData(res.data?.user);
      setLoggedIn(true);
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
