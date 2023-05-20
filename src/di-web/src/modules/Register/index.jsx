import React, { useState } from 'react';
import { Form, Input, Button, Radio, Card, Typography, Row, Col } from 'antd';
import { BASE_URL } from '../../utils/constant/url';
import { registerUser } from './api';

const { Title, Paragraph } = Typography;

const RegistrationForm = () => {
  const [form] = Form.useForm();
  const [gender, setGender] = useState('male');

  // const onFinish = (values) => {
  //   const requestOptions = {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify(values),
  //   };

  //   fetch('http://localhost:8000/auth/team/accept', requestOptions)
  //     .then(response => response.json())
  //     .then(data => console.log(data));
  //   // console.log(values);
  // };33
  
  const onFinish = (values) => {
    registerUser(values)
      .then(data => console.log(data))
      .catch(error => console.error(error));
      // console.log(values);
  };

  return (
    <Row justify="center" align="middle" style={{ minHeight: '100vh' }}>
      <Col xs={20} sm={16} md={12} lg={10} xl={8}>
        <Card>
          <Title level={4} style={{ textAlign: 'center' }}>Welcome to the Digital Health Platform</Title>
        <Paragraph>
          We're delighted to have you on board. Let's start by getting you registered. 
          Please fill in the following information to create a new account.
        </Paragraph>
        <Title level={4} style={{ textAlign: 'center' }}>About Our Project</Title>
        <Paragraph>
          The platform's primary function is to simplify the process of associating free-text descriptions, which generally explain the reasoning behind prescribing specific medications, onto a Universal Indication List (UIL), which serves as a subset of the broader standardized knowledge base of clinical terms called SNOMED CT.
        </Paragraph>
        <Form
          form={form}
          name="register"
          onFinish={onFinish}
          scrollToFirstError
        >
          <Form.Item
            name="invitationCode"
            rules={[
              {
                required: true,
                message: 'Please input your Invitation Code!',
              },
            ]}
          >
            <Input placeholder="Invitation Code" />
          </Form.Item>

          <Form.Item
            name="email"
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
            rules={[
              {
                required: true,
                message: 'Please input your password!',
              },
            ]}
          >
            <Input.Password placeholder="Password" />
          </Form.Item>

          <Form.Item
            name="firstName"
            rules={[
              {
                required: true,
                message: 'Please input your first name!',
              },
            ]}
          >
            <Input placeholder="First Name" />
          </Form.Item>

          <Form.Item
            name="lastName"
            rules={[
              {
                required: true,
                message: 'Please input your last name!',
              },
            ]}
          >
            <Input placeholder="Last Name" />
          </Form.Item>

          <Form.Item
            name="nickname"
            rules={[
              {
                required: true,
                message: 'Please input your nickname!',
              },
            ]}
          >
            <Input placeholder="Nickname" />
          </Form.Item>

          <Form.Item name="gender">
            <Radio.Group onChange={e => setGender(e.target.value)} value={gender} style={{ justifyContent: 'center', display: 'flex' }}>
              <Radio value={'male'}>Male</Radio>
              <Radio value={'female'}>Female</Radio>
              <Radio value={'other'}>Other</Radio>
            </Radio.Group>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" style={{ width: '100%' }}>
              Register
            </Button>
          </Form.Item>
        </Form>
        </Card>
      </Col>
    </Row>
  );
};

export default RegistrationForm;

