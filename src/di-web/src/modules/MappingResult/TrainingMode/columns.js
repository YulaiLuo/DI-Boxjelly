import { useState } from 'react';
import { ToolOutlined } from '@ant-design/icons';
import { UNIVERSAL_INDICATION_LIST } from '../../../utils/constant/indicationList';

/**
 * @see {@link https://procomponents.ant.design/en-US/components/table#columns-column-definition}
 */
export const getColumns = (options) => {
  const filter = (inputValue, path) =>
    path.some((option) => option.label.toLowerCase().indexOf(inputValue.toLowerCase()) > -1);

  return [
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
      // render: (s, row) => {
      //   console.log('ass', s, row);
      //   if (row.curate === null || row.curate === undefined) return '-';
      //   else return row.curate[row.curate.length - 1];
      // },
      valueType: 'cascader',
      fieldProps: (form, config, x) => {
        // console.log('sss', form, config, x);
        return {
          options,
          showSearch: {
            filter,
          },
          displayRender: (labels) => labels[labels.length - 1], // just show the leaf item
        };
      },
    },
    {
      title: 'Action',
      width: '120',
      fixed: 'right',
      valueType: 'option',
      render: (text, record, _, action) => (
        <span
          class="cursor-pointer pl-3"
          key="editable"
          onClick={() => {
            action?.startEditable?.(record.id);
          }}
        >
          <ToolOutlined />
        </span>
      ),
    },
  ];
};
