// Import necessary modules and hooks
import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Select, Row, Col, Typography, message } from 'antd';
import { registerUser } from './api';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

// Component definitions from Ant Design library
const { Option } = Select;
const { Title, Paragraph } = Typography;

// Main component for the Register page
const RegisterPage = () => {
  // Initialize state and hooks
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  // Check if the URL contains an invite token, if yes, auto-fill the input field
  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const inviteToken = searchParams.get('invite_token');
    if (inviteToken) {
      form.setFieldsValue({
        invite_token: inviteToken,
      });
    }
  }, [location, form]);

  // Function to handle form submission
  const onFinish = async (values) => {
    try {
      setLoading(true);
      const formData = new FormData();
      // Append all input field values into a FormData object
      for (const key in values) {
        formData.append(key, values[key]);
      }
      await registerUser(formData); // Send request to server to register user
      setLoading(false);

      // If successful, show message and redirect to login page after 3 seconds
      message.success('Registration successful, redirecting to login page...', 3);
      setTimeout(() => navigate('/login'), 3000); // redirect to login page after 3 seconds
    } catch (error) {
      console.error(error);
      setLoading(false);
      // If there's an error, display the error message
      if (error.response && error.response.data && error.response.data.message) {
        message.error(error.response.data.message);
      } else {
        message.error('An error occurred during registration. Please try again.');
      }
    }
  };

  // The JSX to be rendered
  return (
    // Many more JSX elements
    <Row justify="center" align="middle" style={{ minHeight: '100vh' }}>
      <Col span={8}>
        <Title level={2} style={{ textAlign: 'center' }}>
          Welcome to the Digital Health Platform
        </Title>
        <Paragraph style={{ textAlign: 'center', marginBottom: '2rem' }}>
          We're delighted to have you on board. Let's start by getting you registered. Please fill
          in the following information to create a new account.
        </Paragraph>
        <Form
          form={form}
          name="register"
          onFinish={onFinish}
          scrollToFirstError
          style={{ width: '100%', maxWidth: '400px', margin: 'auto' }}
          layout="vertical"
        >
          <Form.Item
            name="invite_token"
            label="Invite Token"
            rules={[{ required: true, message: 'Please input your invite token!' }]}
          >
            <Input placeholder="Invite Token" disabled={true} />
          </Form.Item>

          <Form.Item
            name="username"
            label="Username"
            rules={[{ required: true, message: 'Please input your username!' }]}
          >
            <Input placeholder="Username" />
          </Form.Item>

          <Form.Item
            name="email"
            label="Email"
            rules={[
              {
                type: 'email',
                message: 'The input is not valid E-mail!',
              },
              {
                required: true,
                message: 'Please input your E-mail!',
              },
            ]}
          >
            <Input placeholder="Email" />
          </Form.Item>

          <Form.Item
            name="password"
            label="Password"
            rules={[
              {
                required: true,
                message: 'Please input your password!',
              },
            ]}
            hasFeedback
          >
            <Input.Password placeholder="Password" />
          </Form.Item>

          <Form.Item
            name="confirm"
            label="Confirm Password"
            dependencies={['password']}
            hasFeedback
            rules={[
              {
                required: true,
                message: 'Please confirm your password!',
              },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }

                  return Promise.reject(
                    new Error('The two passwords that you entered do not match!')
                  );
                },
              }),
            ]}
          >
            <Input.Password placeholder="Confirm Password" />
          </Form.Item>

          <Form.Item
            name="first_name"
            label="First Name"
            rules={[{ required: true, message: 'Please input your first name!' }]}
          >
            <Input placeholder="First Name" />
          </Form.Item>

          <Form.Item
            name="last_name"
            label="Last Name"
            rules={[{ required: true, message: 'Please input your last name!' }]}
          >
            <Input placeholder="Last Name" />
          </Form.Item>

          <Form.Item
            name="gender"
            label="Gender"
            rules={[{ required: true, message: 'Please select your gender!' }]}
          >
            <Select placeholder="Gender">
              <Option value="Male">Male</Option>
              <Option value="Female">Female</Option>
              <Option value="Other">Other</Option>
            </Select>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} style={{ width: '100%' }}>
              Register
            </Button>
          </Form.Item>
        </Form>
      </Col>
    </Row>
  );
};

export default RegisterPage;
