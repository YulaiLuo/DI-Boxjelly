import React, { useState, useEffect } from 'react';
import { EditableProTable } from '@ant-design/pro-components';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';

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
      key: 'name',
      dataIndex: 'name',
      valueType: 'text',
      formItemProps: () => {
        return {
          rules: [{ required: true, message: 'must be filled' }],
        };
      },
    },
    {
      title: 'Tags',
      key: 'description',
      dataIndex: 'description',
      valueType: 'text',
    },
    {
      title: 'Actions',
      valueType: 'option',
      width: 200,
      render: (text, record, _, action) => [
        <a
          key="editable"
          onClick={() => {
            action?.startEditable?.(record.id);
          }}
        >
          <EditOutlined />
        </a>,
        <a
          key="delete"
          onClick={() => {
            setDataSource(dataSource.filter((item) => item.id !== record.id));
          }}
        >
          <DeleteOutlined />
        </a>,
      ],
    },
  ];

  return (
    <div>
      <EditableProTable
        rowKey="id"
        columns={columns}
        value={dataSource}
        editable={{
          type: 'multiple',
          editableKeys,
          onSave: async (rowKey, data, row) => {
            // TODO
            console.log(rowKey, data, row);
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
