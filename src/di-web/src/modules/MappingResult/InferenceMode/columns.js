export const columns = [
  {
    title: 'Original Text',
    dataIndex: 'originalText',
    key: 'originalText',
    ellipsis: {
      showTitle: false,
    },
  },
  {
    title: 'Mapping Category',
    dataIndex: 'mappedText',
    key: 'mappedText',
    ellipsis: {
      showTitle: false,
    },
    render: (text, record) => {
      if (record.mappingStatus === 0) return '-';
      else return text;
    },
  },
];
