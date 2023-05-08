import React from 'react';
import { PropTypes } from 'prop-types';
import { Card, Badge, Popconfirm } from 'antd';
import { EditOutlined, DeleteOutlined, BarChartOutlined } from '@ant-design/icons';

const TaskCard = ({ id, status, num, createBy, createAt, updateAt, onEditClick }) => {
  const badgeStatus = {
    success: 'success',
    fail: 'error',
    pending: 'processing',
  };

  const title = (
    <div class="flex justify-between">
      <span>{createBy}</span>
      <Badge status={badgeStatus[status]} text={status}></Badge>
    </div>
  );

  const onVisualizeClick = () => {
    console.log('visualize');
  };

  const onDeleteClick = () => {
    console.log('delete');
  };

  return (
    <Card
      title={title}
      // hoverable={true}
      actions={[
        <EditOutlined key="edit" onClick={onEditClick} />,
        <BarChartOutlined key="visualization" onClick={onVisualizeClick} />,
        <Popconfirm
          placement="bottom"
          title={'Are you sure you want to delete this task?'}
          description={'Delete this task'}
          onConfirm={onDeleteClick}
          okText="Yes"
          cancelText="No"
        >
          <DeleteOutlined key="delete" />,
        </Popconfirm>,
      ]}
    >
      <div class="h-24">
        <div class="flex items-center">
          <span>Mapping number:</span>
          <span class="ml-4 text-xl">{num}</span>
        </div>
        <div>Task ID: {id}</div>
        <div>Created at: {createAt}</div>
        {updateAt && <div>Updated: at: {updateAt}</div>}
      </div>
    </Card>
  );
};

export default TaskCard;

TaskCard.propTypes = {
  id: PropTypes.string.isRequired,
  status: PropTypes.oneOf(['success', 'fail', 'pending']).isRequired,
  num: PropTypes.number,
  createBy: PropTypes.string.isRequired,
  createAt: PropTypes.string.isRequired,
  updateAt: PropTypes.string,
};
