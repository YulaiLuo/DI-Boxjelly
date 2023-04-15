import React, {useEffect} from 'react';
import { useLocation,  useNavigate } from 'react-router-dom';
import { Tabs } from 'antd';
import InferenceMode from './InferenceMode';

export default function MappingResult() {
  
  const navigate = useNavigate();
  const {state} = useLocation();
  const defaultActiveKey = state.mappingMode === 1 ? 'training' : 'inference';
  const data = state.mappingRes ?? [];
  
  const items = [
    {
      key: 'inference',
      label: `Inference`,
      children: <InferenceMode data={data}/>,
    },
    {
      key: 'training',
      label: `Training`,
      children: `training`,
    },
  ]

  useEffect(() => {
    if (state === null) {
      navigate('/', {replace: true})
    }
  }, [])

  
  return (
    <div class='px-8 py-4'>
      <Tabs defaultActiveKey={defaultActiveKey} items={items} onChange={() =>{}} tabBarGutter={30} />
    </div>
  )
}
