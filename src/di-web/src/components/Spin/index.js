import React from 'react';
import { Spin } from 'antd';
import { PropTypes } from 'prop-types';

export default function SpinInContainer({ size = 'default' }) {
  return (
    <div class="flex items-center justify-center h-full">
      <Spin size={size} />
    </div>
  );
}

SpinInContainer.propTypes = {
  size: PropTypes.oneOf(['small', 'default', 'large']),
};
