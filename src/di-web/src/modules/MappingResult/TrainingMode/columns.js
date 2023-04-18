import { Space, Badge, Tooltip, Cascader, Input } from 'antd';
import { EyeOutlined, ToolOutlined } from '@ant-design/icons';
import { UNIVERSAL_INDICATION_LIST } from '../../../utils/constant/indicationList';

const options = UNIVERSAL_INDICATION_LIST.map((item) => {
  return {
    value: item.group,
    label: item.group,
    children: item.children.map((child) => ({
      value: child,
      label: child,
    })),
  };
});

/**
 * @see {@link https://procomponents.ant.design/en-US/components/table#columns-column-definition}
 */
export const columns = [
  {
    title: 'Original Text',
    dataIndex: 'originalDisplay',
    key: 'originalDisplay',
    width: '25%',
    ellipsis: {
      showTitle: true,
    },
    readonly: true,
    render: (text, record) => (
      <Tooltip
        placement="topLeft"
        title={<span style={{ color: '#fff' }}>{record.originalDisplay}</span>}
      >
        {text}
      </Tooltip>
    ),
  },
  {
    title: 'Mapping Category',
    dataIndex: 'display',
    key: 'display',
    width: '25%',
    ellipsis: {
      showTitle: true,
    },
    readonly: true,
    render: (text, record) => {
      if (record.mappingSuccess)
        return (
          <Tooltip
            placement="topLeft"
            title={<span style={{ color: '#fff' }}>{record.display}</span>}
          >
            {text}
          </Tooltip>
        );
      else return '-';
    },
  },
  {
    title: 'Curated Category',
    key: 'curatedCategory',
    dataIndex: 'curatedCategory',
    render: (_, row) => {
      if (row.curatedCategory === null || row.curatedCategory === undefined) return '-';
      else return row.curatedCategory[row.curatedCategory.length - 1];
    },
    valueType: 'cascader',
    fieldProps: {
      options,
      displayRender: (labels) => labels[labels.length - 1], // just show the leaf item
    },
  },
  {
    title: 'Mapping Status',
    dataIndex: 'mappingSuccess',
    key: 'mappingSuccess',
    width: '15%',
    ellipsis: true,
    readonly: true,
    render: (_, record) => {
      if (record.mappingSuccess === true) return <Badge status="success" text="Success" />;
      else return <Badge status="error" text="Fail" />;
    },
  },
  {
    title: 'Action',
    width: '15%',
    valueType: 'option',
    render: (text, record, _, action) => (
      <Space size="middle">
        <span
          class="cursor-pointer"
          key="editable"
          onClick={() => {
            console.log(action?.startEditable);
            action?.startEditable?.(record.id);
          }}
        >
          <ToolOutlined />
        </span>
        <span class="cursor-pointer">
          <EyeOutlined />
        </span>
      </Space>
    ),
  },
];
