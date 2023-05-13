import React from 'react';
import { Drawer, Col, Row, Card } from 'antd';
import {
  PieChart,
  Pie,
  BarChart,
  Bar,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Cell,
} from 'recharts';

export default function VisualizationDrawer({ onClose, open, metaData, width = 900 }) {
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

  return (
    <Drawer title="Overall Performance" width={width} onClose={onClose} open={open}>
      <Row gutter={16}>
        <Col span={12} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Card
            bordered={true}
            style={{
              width: 300,
            }}
          >
            <div>
              <h4>Total Mapping Text: {num}</h4>
              <h4>
                Successful Mapping Rate: {num > 0 ? ((num_success / num) * 100).toFixed(2) : 0} %
              </h4>
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
        </Col>
        <Col span={12} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <PieChart width={400} height={400}>
            <Pie
              data={chartData}
              cx={200}
              cy={200}
              innerRadius={60}
              outerRadius={80}
              fill="#8884d8"
              paddingAngle={5}
              dataKey="value"
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(2)}%`}
              labelLine={false}
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={
                    entry.name === 'Success' ? 'green' : entry.name === 'Failed' ? 'red' : 'orange'
                  }
                />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </Col>
        <Col span={12} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <BarChart width={400} height={300} data={transformedChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Success" fill="green" />
            <Bar dataKey="Failed" fill="red" />
            <Bar dataKey="Reviewed" fill="orange" />
          </BarChart>
        </Col>
        <Col span={12} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <ScatterChart
            width={400}
            height={400}
            margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" type="category" allowDuplicatedCategory={false} />
            <YAxis dataKey="value" type="number" name="value" />
            <Tooltip />
            <Legend />
            <Scatter data={chartData} shape={renderCustomizedShape} line />
          </ScatterChart>
        </Col>
      </Row>
    </Drawer>
  );
}
