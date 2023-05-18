import React from 'react';
import { PropTypes } from 'prop-types';
import { Card, Badge, Popconfirm } from 'antd';
import { DeleteOutlined, BarChartOutlined, DownloadOutlined } from '@ant-design/icons';
import { formatTime, calTimeDifference } from '../../../utils/formatTime';

const TaskCard = ({ item, onEditClick, onDownloadClick, onDeleteClick, onVisualizeClick }) => {
  const { status, num, createBy, createAt, updateAt, fileName } = item;

  const badgeStatus = {
    success: 'success',
    fail: 'error',
    pending: 'processing',
  };

  const title = (
    <div class="flex justify-between">
      {/* <span class="w-3/5 overflow-hidden text-ellipsis">{createBy}</span> */}
      <span class="w-3/5 overflow-hidden text-ellipsis">{'Vlada'}</span>
      <Badge status={badgeStatus[status]} text={status}></Badge>
    </div>
  );

  const CreatTime = new Date(createAt);
  const UpdateTime = new Date(updateAt);

  const formattedCreateAt = formatTime(CreatTime);
  const formattedUpdateAt = updateAt ? formatTime(new Date(updateAt)) : null;

  const currentTime = new Date();
  const timeDifference = Math.abs(currentTime - UpdateTime);

  const formattedTimeDifference = calTimeDifference(timeDifference);

  const getActions = () => {
    let actions = [
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
    ];
    if (status === 'success') {
      actions = [
        <DownloadOutlined key="download" onClick={onDownloadClick} />,
        <BarChartOutlined key="visualization" onClick={onVisualizeClick} />,
        ...actions,
      ];
    }
    return actions;
  };

  return (
    <Card title={title} bordered={false} actions={getActions()}>
      <div
        class={`min-h-24 overflow-auto ${
          status === 'success' ? 'cursor-pointer' : 'cursor-not-allowed'
        }`}
        onClick={() => {
          if (status === 'success') {
            onEditClick();
          }
        }}
      >
        <div class="flex items-center">
          <span>Mapping number:</span>
          <span class="ml-4 text-lg">{num}</span>
        </div>
        <div>File name: {fileName}</div>
        <div>Created at: {formattedCreateAt}</div>
        {/* <div>Last curated time: {formattedTimeDifference}</div> */}
        {createAt !== updateAt && <div>Last curated time: {formattedTimeDifference}</div>}
      </div>
    </Card>
  );
};

export default TaskCard;

TaskCard.propTypes = {
  item: PropTypes.shape({
    id: PropTypes.string.isRequired,
    status: PropTypes.oneOf(['success', 'fail', 'pending']).isRequired,
    num: PropTypes.number,
    createBy: PropTypes.string.isRequired,
    createAt: PropTypes.string.isRequired,
    updateAt: PropTypes.string,
  }).isRequired,
  onEditClick: PropTypes.func,
  onDownloadClick: PropTypes.func,
  onDeleteClick: PropTypes.func,
  onVisualizeClick: PropTypes.func,
};
