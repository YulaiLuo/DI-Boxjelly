import React from 'react';
import { Collapse, Button } from 'antd';
import { useRequest } from 'ahooks';
import { UNIVERSAL_INDICATION_LIST } from '../../utils/constant/indicationList';
import CodeCard from './components/CodeCard';
import { getCodeSystemList } from './api';

const { Panel } = Collapse;

export default function CodeSystem() {
  const { data: codeSystemList } = useRequest(() => getCodeSystemList('1234', 'code_system_id'));

  console.log(codeSystemList);

  const groups = codeSystemList?.data?.groups ?? [];

  const data = codeSystemList?.data?.groups[0].concepts;
  const group = codeSystemList?.data?.groups[0].group;

  console.log(data);

  return (
    <div class="m-4">
      <div class="mb-4 flex flex-row-reverse">
        <Button type="primary">Add a new group</Button>
      </div>
      <div>
        <Collapse>
          {groups.map((item, i) => {
            return (
              <Panel header={group} key={i}>
                <CodeCard data={data ?? []} />
              </Panel>
            );
          })}
        </Collapse>
        {/* <CodeCard data={data ?? []} groupName={group} /> */}
      </div>
    </div>
  );
}
