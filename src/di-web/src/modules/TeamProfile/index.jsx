import React from 'react';
import { List, Avatar, Layout, Menu, Button } from 'antd';
import { useRequest } from 'ahooks';
import { getTeamInfo } from './api';
import { BASE_URL } from '../../utils/constant/url';

const { Sider, Content } = Layout;

export default function TeamProfile() {
  const teamId = localStorage.getItem('team');

  const { data: teamInfo } = useRequest(() => getTeamInfo(teamId));

  const data = teamInfo?.data;

  const getSidebarItem = (label, key, icon, children) => ({
    label,
    key,
    children,
    icon,
  });

  const sidebarItems = [getSidebarItem('All members', 'all'), getSidebarItem('Pending', 'pending')];

  return (
    <div class="mx-4 py-3">
      <div class="flex items-center justify-between">
        <h2 class="mr-5">Team {data?.team_name} </h2>
        <Button type="primary">Invite Member</Button>
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
