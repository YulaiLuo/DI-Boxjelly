export const columns = [
  {
    title: 'Original Text',
    dataIndex: 'originalDisplay',
    key: 'originalDisplay',
  },
  {
    title: 'Mapping Category',
    dataIndex: 'display',
    key: 'display',
    render: (text, record) => {
      if (record.mappingSuccess) return text;
      else return '-';
    },
  },
];
