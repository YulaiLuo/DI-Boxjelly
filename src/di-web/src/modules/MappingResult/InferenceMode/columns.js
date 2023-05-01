export const columns = [
  {
    title: 'Original Text',
    dataIndex: 'originalDisplay',
    key: 'originalDisplay',
    ellipsis: {
      showTitle: false,
    },
  },
  {
    title: 'Mapping Category',
    dataIndex: 'display',
    key: 'display',
    ellipsis: {
      showTitle: false,
    },
    render: (text, record) => {
      if (record.mappingSuccess) return text;
      else return '-';
    },
  },
];
