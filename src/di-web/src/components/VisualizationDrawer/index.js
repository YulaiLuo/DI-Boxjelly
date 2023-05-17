import React, { useState, useEffect } from 'react';
import { Drawer, Col, Row, Card } from 'antd';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell } from 'recharts';

export default function VisualizationDrawer({ onClose, open, metaData }) {
  const num = metaData?.data.num;
  const num_success = metaData?.data.num_success;
  const num_failed = metaData?.data.num_failed;
  const num_reviewed = metaData?.data.num_reviewed;

  const chartData = [
    { name: 'Success', value: num_success },
    { name: 'Failed', value: num_failed },
    { name: 'Reviewed', value: num_reviewed },
  ];

  const transformedChartData = [
    { name: 'Success', Success: num_success },
    { name: 'Failed', Failed: num_failed },
    { name: 'Reviewed', Reviewed: num_reviewed },
  ];

  const renderCustomizedShape = (props) => {
    const { cx, cy, name } = props;
    let fill;
    switch (name) {
      case 'Success':
        fill = 'green';
        break;
      case 'Failed':
        fill = 'red';
        break;
      case 'Reviewed':
        fill = 'orange';
        break;
      default:
        fill = 'gray';
    }
    return <circle cx={cx} cy={cy} r={6} fill={fill} />;
  };

  const GreenDot = () => {
    const dotGreen = {
      display: 'inline-block',
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: 'green',
      marginRight: '10px',
    };

    return <div style={dotGreen}></div>;
  };

  const RedDot = () => {
    const dotRed = {
      display: 'inline-block',
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: 'red',
      marginRight: '10px',
    };

    return <div style={dotRed}></div>;
  };

  const OrangeDot = () => {
    const dotOrange = {
      display: 'inline-block',
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: 'orange',
      marginRight: '10px',
    };

    return <div style={dotOrange}></div>;
  };

  const StatisticsCard = ({ num, num_success, num_failed, num_reviewed }) => (
    <Card
      bordered={true}
      style={{ width: '90%', margin: '0 auto', marginBottom: '5vh', left: '5%' }}
    >
      <div>
        <h4>Total Mapping Text: {num}</h4>
        <h4>Successful Mapping Rate: {num > 0 ? ((num_success / num) * 100).toFixed(2) : 0} %</h4>
      </div>
      <div>
        <GreenDot />
        Number of Success: {num_success}
      </div>
      <div>
        <RedDot />
        Number of Failure: {num_failed}
      </div>
      <div>
        <OrangeDot />
        Number of Reviewed: {num_reviewed}
      </div>
    </Card>
  );

  const CustomBarChart = ({ data }) => {
    const [chartWidth, setChartWidth] = useState(
      window.innerWidth < 768 ? window.innerWidth * 0.6 : window.innerWidth * 0.3
    );

    useEffect(() => {
      const handleResize = () => {
        setChartWidth(window.innerWidth < 768 ? window.innerWidth * 0.6 : window.innerWidth * 0.3);
      };

      window.addEventListener('resize', handleResize);

      // Cleanup the event listener on component unmount
      return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
      <BarChart width={chartWidth} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="Success" fill="green" />
        <Bar dataKey="Failed" fill="red" />
        <Bar dataKey="Reviewed" fill="orange" />
      </BarChart>
    );
  };

  return (
    <Drawer title="Overall Performance" width={'70vw'} onClose={onClose} open={open}>
      <Row gutter={16}>
        <Col xs={24} md={12} style={{ marginBottom: '30px' }}>
          <StatisticsCard
            num={num}
            num_success={num_success}
            num_failed={num_failed}
            num_reviewed={num_reviewed}
          />
          <CustomBarChart data={transformedChartData} />
        </Col>
        <Col xs={24} md={12} style={{ marginBottom: '30px' }}>
          <StatisticsCard
            num={num}
            num_success={num_success}
            num_failed={num_failed}
            num_reviewed={num_reviewed}
          />
          <CustomBarChart data={transformedChartData} />
        </Col>
      </Row>
    </Drawer>
  );
}
