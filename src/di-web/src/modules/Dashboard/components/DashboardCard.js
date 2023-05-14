import React from 'react';
import { Card, Progress } from 'antd';

export default function DashboardCard({ title, percent, totalNumber }) {
  return (
    <Card title={title}>
      <div class="flex justify-between items-center">
        <div>
          <h1>{totalNumber}</h1>
          <span>+16% since last week</span>
        </div>
        <Progress type="circle" percent={percent} strokeColor="green" />
      </div>
    </Card>
  );
}
