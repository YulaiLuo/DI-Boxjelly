// Importing required dependencies
import React, { useState, useEffect } from 'react';
import { Tag } from 'antd';
import { EditableProTable } from '@ant-design/pro-components';

// The CodeCard component that displays the details of a specific code in an editable table
export default function CodeCard({ data }) {
  // State variables for editable row keys and data source
  const [editableKeys, setEditableRowKeys] = useState([]);
  const [dataSource, setDataSource] = useState([]);

  // useEffect to set data source and reset editable keys when data prop changes
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

  // Columns configuration for the table
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

  // Render the editable table with specified configuration
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
