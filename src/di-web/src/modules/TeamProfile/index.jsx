import React, { useState } from 'react';
import copy from 'copy-to-clipboard';
import { List, Avatar, Layout, Button, notification, message, Tag } from 'antd';
import { SmileOutlined } from '@ant-design/icons';
import { useRequest } from 'ahooks';
import { getTeamInfo, getInvitationLink, deleteTeamMember } from './api';
import { BASE_URL, DOMAIN_URL } from '../../utils/constant/url';
import { useMessageStore } from '../../store';

const { Content } = Layout;

export default function TeamProfile() {
  const teamId = localStorage.getItem('team');
  const userId = localStorage.getItem('user');
  const msgApi = useMessageStore((state) => state.msgApi);

  const { data: teamInfo, refresh: refreshGetTeamInfo } = useRequest(() => getTeamInfo(teamId));
  const data = teamInfo?.data;
  const members = teamInfo?.data?.members ?? [];
  const owner = members.filter((member) => member?.role === 'owner')[0];
  const isOwner = userId === owner?.user_id;

  const { run: runDeleteTeamMember } = useRequest(deleteTeamMember, {
    manual: true,
    onSuccess: () => {
      msgApi.success('Remove user successfully!');
      refreshGetTeamInfo();
    },
  });

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
    const link = DOMAIN_URL + '/register?invite_token=' + result.data;
    const isCopySuccess = copy(link);
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
                <List.Item
                  actions={
                    isOwner &&
                    item.user_id !== userId && [
                      <Button
                        key="remove"
                        type="link"
                        onClick={() => runDeleteTeamMember(teamId, item.user_id)}
                      >
                        Remove
                      </Button>,
                    ]
                  }
                >
                  <List.Item.Meta
                    style={{ display: 'flex', alignItems: 'center' }}
                    avatar={
                      <Avatar
                        // class="mt-4"
                        src={`${BASE_URL}/auth/user/avatar?avatar=${item.avatar}`}
                      />
                      // <Avatar class="mt-4" src={`https://xsgames.co/randomusers/avatar.php?g=pixel&key=${index}`} />
                    }
                    title={
                      <>
                        <span class="mr-2">{item.nickname}</span>
                        <Tag color={item.role === 'owner' ? 'volcano' : 'blue'}>{item.role}</Tag>
                      </>
                    }
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
