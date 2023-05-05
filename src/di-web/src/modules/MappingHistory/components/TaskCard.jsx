import React from 'react';
import { PropTypes } from 'prop-types';
import { Card, Badge } from 'antd';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';

const TaskCard = ({ id, status, num, createBy, createAt, updateAt }) => {
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

  return (
    <Card
      title={title}
      hoverable={true}
      actions={[<EditOutlined key="edit" />, <DeleteOutlined key="delete" />]}
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
