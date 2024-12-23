// Importing required modules
import React from 'react';
import { Card, Progress } from 'antd';

// DashboardCard is a functional component that displays some key statistics
export default function DashboardCard({ title, percent, totalNumber, delta }) {
  return (
    <Card title={title}>
      <div class="flex justify-between items-center">
        <div>
          <h1>{totalNumber}</h1>
          <span>{delta}</span>
        </div>
        <Progress
          type="circle"
          percent={300}
          strokeColor="green"
          format={() => `${Number(percent).toFixed(2)} %`}
        />
      </div>
    </Card>
  );
}
