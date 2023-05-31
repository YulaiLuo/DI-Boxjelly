import React, { useState, useEffect } from 'react';
import { List, Avatar, Layout, Modal, Button, notification, message } from 'antd';
import { SmileOutlined } from '@ant-design/icons';
import { useRequest } from 'ahooks';
import { getTeamInfo, getInvitationLink } from './api';
import { BASE_URL } from '../../utils/constant/url';
import copy from 'copy-to-clipboard';

const { Sider, Content } = Layout;

export default function TeamProfile() {
  const teamId = localStorage.getItem('team');
  const userId = localStorage.getItem('user');
  const { data: teamInfo } = useRequest(() => getTeamInfo(teamId));
  const data = teamInfo?.data;

  const [invitationToken, setInvitationToken] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const [api, contextHolder] = notification.useNotification();
  const openNotification = () => {
    api.open({
      message: 'Invitation link copied to your clipboard!',
      description: 'This link will be expired by 24 hours.',
      icon: (
        <SmileOutlined
          style={{
            color: '#108ee9',
          }}
        />
      ),
    });
  };

  const copyInvitationToken = async () => {
    setIsLoading(true);
    const result = await getInvitationLink(teamId);
    setInvitationToken(result.data);
    const isCopySuccess = copy(result.data);
    if (isCopySuccess) {
      openNotification();
    } else {
      message.error('Please try again！');
    }
    setIsLoading(false);
  };

  return (
    <div class="mx-4 py-3">
      <div class="flex items-center justify-between">
        <h2 class="mr-5">Team {data?.team_name} </h2>
        {contextHolder}
        <Button type="primary" disabled={isLoading} onClick={copyInvitationToken}>
          Invite Member
        </Button>
      </div>
      <Layout>
        <Layout>
          <Content class="ml-3">
            <List
              itemLayout="horizontal"
              dataSource={data?.members}
              renderItem={(item, index) => (
                <List.Item actions={[<a key="remove">Remove</a>, <a key="leave">Leave</a>]}>
                  <List.Item.Meta
                    style={{ display: 'flex', alignItems: 'center' }}
                    avatar={
                      <Avatar
                        // class="mt-4"
                        src={`${BASE_URL}/auth/user/avatar?avatar=${item.avatar}`}
                      />
                      // <Avatar class="mt-4" src={`https://xsgames.co/randomusers/avatar.php?g=pixel&key=${index}`} />
                    }
                    title={item.nickname}
                    description={item.email}
                  />
                </List.Item>
              )}
            />
          </Content>
        </Layout>
      </Layout>
    </div>
  );
}
