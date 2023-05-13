import { Space } from 'antd';
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
    title: 'Raw text',
    dataIndex: 'originalText',
    key: 'originalText',
    width: 260,
    ellipsis: {
      showTitle: true,
    },
    readonly: true,
  },
  {
    title: 'Output of the mapping tool',
    dataIndex: 'mappedText',
    key: 'mappedText',
    width: 260,
    ellipsis: {
      showTitle: true,
    },
    readonly: true,
  },
  {
    title: 'Confidence',
    key: 'confidence',
    dataIndex: 'confidence',
    readonly: true,
  },
  {
    title: 'Source',
    key: 'source',
    dataIndex: 'source',
    readonly: true,
  },
  {
    title: 'Status',
    dataIndex: 'mappingStatus',
    key: 'mappingStatus',
    ellipsis: true,
    readonly: true,
    valueType: 'select',
    valueEnum: {
      0: { text: 'Fail', status: 'Error' },
      1: {
        text: 'Success',
        status: 'Success',
      },
      2: {
        text: 'Reviewed',
        status: 'warning',
      },
    },
  },
  {
    title: 'Curated Category',
    key: 'curate',
    dataIndex: 'curate',
    width: 260,
    render: (_, row) => {
      if (row.curate === null || row.curate === undefined) return '-';
      else return row.curate[row.curate.length - 1];
    },
    valueType: 'cascader',
    fieldProps: {
      options,
      displayRender: (labels) => labels[labels.length - 1], // just show the leaf item
    },
  },
  {
    title: 'Action',
    width: '120',
    fixed: 'right',
    valueType: 'option',
    render: (text, record, _, action) => (
      <Space size="middle">
        <span
          class="cursor-pointer"
          key="editable"
          onClick={() => {
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
