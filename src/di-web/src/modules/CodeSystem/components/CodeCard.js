import React, { useState, useEffect } from 'react';
import { Tag } from 'antd';
import { EditableProTable } from '@ant-design/pro-components';

export default function CodeCard({ data }) {
  const [editableKeys, setEditableRowKeys] = useState([]);
  const [dataSource, setDataSource] = useState([]);

  useEffect(() => {
    setDataSource(
      data.map((v, i) => {
        return {
          ...v,
          id: i,
        };
      })
    );
    setEditableRowKeys([]);
  }, [data]);

  const columns = [
    {
      title: 'Indication',
      key: 'concept_name',
      dataIndex: 'concept_name',
      valueType: 'text',
      formItemProps: () => {
        return {
          rules: [{ required: true, message: 'must be filled' }],
        };
      },
    },
    {
      title: 'User Alias',
      key: 'alias',
      dataIndex: 'alias',
    },
    {
      title: 'Tags',
      key: 'tags',
      dataIndex: 'tags',
      render: (_, { tags }) => (
        <>
          {tags?.map((tag) => {
            return <Tag key={tag}>{tag}</Tag>;
          })}
        </>
      ),
    },
  ];

  return (
    <div>
      <EditableProTable
        rowKey="id"
        columns={columns}
        value={dataSource}
        maxLength={dataSource.length}
        editable={{
          type: 'multiple',
          editableKeys,
          onSave: async (rowKey, data, row) => {
            // TODO
            data.mappingStatus = 2;
          },
          onChange: setEditableRowKeys,
          // actionRender: (row, config, dom) => [dom.save, dom.cancel],
        }}
        onChange={setDataSource}
        // maxLength={dataSource.length}
        // scroll={{ y: 200 }}
        recordCreatorProps={{
          record: (index) => {
            return { id: index + 1 };
          },
        }}
      />
    </div>
  );
}
