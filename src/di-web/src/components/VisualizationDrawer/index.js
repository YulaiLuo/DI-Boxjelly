import React, { useState, useEffect } from 'react';
import { Drawer, Col, Row, Card } from 'antd';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell } from 'recharts';

export default function VisualizationDrawer({ onClose, open, metaData }) {
  const num = metaData?.data.num;
  const num_success = metaData?.data.num_success;
  const num_failed = metaData?.data.num_failed;
  const num_reviewed = metaData?.data.num_reviewed;
  const num_uil = metaData?.data.num_uil;
  const num_snomed = metaData?.data.num_snomed;

  const chartData = [
    { name: 'Success', Success: num_success },
    { name: 'Failed', Failed: num_failed },
    { name: 'Reviewed', Reviewed: num_reviewed },
  ];

  const transformedChartData = [
    { name: 'UIL', UIL: num_uil },
    { name: 'SNOMED', SNOMED: num_snomed },
  ];

  // const renderCustomizedShape = (props) => {
  //   const { cx, cy, name } = props;
  //   let fill;
  //   switch (name) {
  //     case 'Success':
  //       fill = 'green';
  //       break;
  //     case 'Failed':
  //       fill = 'red';
  //       break;
  //     case 'Reviewed':
  //       fill = 'orange';
  //       break;
  //     default:
  //       fill = 'gray';
  //   }
  //   return <circle cx={cx} cy={cy} r={6} fill={fill} />;
  // };

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

  const BlueDot = () => {
    const dotBlue = {
      display: 'inline-block',
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: 'blue',
      marginRight: '10px',
    };

    return <div style={dotBlue}></div>;
  };

  const BlackDot = () => {
    const dotBlack = {
      display: 'inline-block',
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: 'black',
      marginRight: '10px',
    };

    return <div style={dotBlack}></div>;
  };

  const WhiteDot = () => {
    const dotWhtie = {
      display: 'inline-block',
      width: '10px',
      height: '10px',
      borderRadius: '50%',
      backgroundColor: 'whtie',
      marginRight: '10px',
    };

    return <div style={dotWhtie}></div>;
  };

  const StatisticsCard1 = ({ num, num_success, num_failed, num_reviewed }) => (
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

  const StatisticsCard2 = ({ num_success, num_uil, num_snomed }) => (
    <Card
      bordered={true}
      style={{ width: '90%', margin: '0 auto', marginBottom: '5vh', left: '5%' }}
    >
      <div>
        <h4>UIL Mapping Ratio : {num_success > 0 ? ((num_uil / num_success) * 100).toFixed(2) : 0} %</h4>
        <h4>SNOMED CT Mapping Ratio: {num_success > 0 ? ((num_snomed / num_success) * 100).toFixed(2) : 0} %</h4>
      </div>
      <div>
        <BlueDot />
        Number of UIL: {num_uil}
      </div>
      <div>
        <BlackDot />
        Number of SNOMED CT: {num_snomed}
      </div>
      <div>
        <WhiteDot />
      </div>
    </Card>
  );

  const CustomBarChart1 = ({ data }) => {
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

  const CustomBarChart2 = ({ data }) => {
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
        <CartesianGrid strokeDasharray="2 2" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="UIL" fill="blue" />
        <Bar dataKey="SNOMED" fill="black" />
      </BarChart>
    );
  };

  return (
    <Drawer title="Overall Performance" width={'70vw'} onClose={onClose} open={open}>
      <Row gutter={16}>
        <Col xs={24} md={12} style={{ marginBottom: '30px' }}>
          <StatisticsCard1
            num={num}
            num_success={num_success}
            num_failed={num_failed}
            num_reviewed={num_reviewed}
          />
          <CustomBarChart1 data={chartData} />
        </Col>
        <Col xs={24} md={12} style={{ marginBottom: '30px' }}>
          <StatisticsCard2
            num_success={num_success}
            num_uil={num_uil}
            num_snomed={num_snomed}
          />
          <CustomBarChart2 data={transformedChartData} />
        </Col>
      </Row>
    </Drawer>
  );
}
