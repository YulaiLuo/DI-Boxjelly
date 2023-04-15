import React from 'react';
import { Table, Button } from 'antd';
import { columns as InferenceColumns } from './columns';

export default function InferenceMode({ data }) {
  return (
    <>
      <div class="flex flex-row-reverse">
        <Button type="primary" size="large">
          Export
        </Button>
      </div>
      <Table columns={InferenceColumns} dataSource={data} size="middle" />
    </>
  );
}
