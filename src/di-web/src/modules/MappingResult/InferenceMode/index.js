import React from 'react';
import { Table, Button } from 'antd';
import { columns as InferenceColumns } from './columns';
import { exportFile } from '../../Mapping/api';

export default function InferenceMode({ data, taskId }) {
  return (
    <>
      <div class="flex flex-row-reverse">
        <Button type="primary" size="large" onClick={() => exportFile(teamId, taskId)}>
          Export
        </Button>
      </div>
      <Table columns={InferenceColumns} dataSource={data} size="middle" />
    </>
  );
}
