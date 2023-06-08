import React from 'react';
import { PropTypes } from 'prop-types';
import { Card, Badge, Popconfirm } from 'antd';
import { DeleteOutlined, BarChartOutlined, DownloadOutlined } from '@ant-design/icons';
import { formatTime, calTimeDifference } from '../../../utils/formatTime';

// TaskCard is a React component that represents an individual task within a mapping project.
// This component receives a task item and callback functions for various user interactions as props.
const TaskCard = ({ item, onEditClick, onDownloadClick, onDeleteClick, onVisualizeClick }) => {
  const { status, num, nickname, createAt, updateAt, fileName } = item;

  // Define badge status colors for different statuses.
  const badgeStatus = {
    success: 'success',
    fail: 'error',
    pending: 'processing',
  };

  // Define the title of the task card.
  const title = (
    <div class="flex justify-between">
      <span class="w-3/5 overflow-hidden text-ellipsis">{nickname}</span>
      <Badge
        status={badgeStatus[status]}
        text={status.charAt(0).toUpperCase() + status.slice(1)}
      ></Badge>
    </div>
  );

  // Calculate and format the creation time of the task.
  const CreatTime = new Date(createAt);
  const formattedCreateAt = formatTime(CreatTime);

  // Calculate and format the time difference between now and the creation time.
  const currentTime = new Date();
  const timeDifference = Math.abs(currentTime - CreatTime);
  const formattedTimeDifference = calTimeDifference(timeDifference);

  // Determine the set of action icons for the card based on the task status.
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

  // Render the task card with the title, formatted time information, and the appropriate set of action icons.
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
        <div>Created at: {formattedTimeDifference}</div>
        <div>{formattedCreateAt}</div>
      </div>
    </Card>
  );
};

export default TaskCard;

// Define the types of the props passed to the TaskCard component.
TaskCard.propTypes = {
  item: PropTypes.shape({
    id: PropTypes.string.isRequired,
    status: PropTypes.oneOf(['success', 'fail', 'pending']).isRequired,
    num: PropTypes.number,
    createBy: PropTypes.string.isRequired,
    createAt: PropTypes.string.isRequired,
    updateAt: PropTypes.string,
  }).isRequired,
  // onEditClick is a function that gets called when a user clicks to edit this task.
  onEditClick: PropTypes.func,
  // onDownloadClick is a function that gets called when a user clicks to download the data of this task.
  onDownloadClick: PropTypes.func,
  // onDeleteClick is a function that gets called when a user confirms the deletion of this task.
  onDeleteClick: PropTypes.func,
  // onVisualizeClick is a function that gets called when a user clicks to visualize the data of this task.
  onVisualizeClick: PropTypes.func,
};
