// mapped task detail
export const mapTaskDetail = [
  {
    mapped_info: [
      {
        confidence: 0.9971789121627808,
        end_index: 9,
        sct_code: '420008001',
        sct_term: 'Travel',
        similarity: 1.0,
        start_index: 3,
        status: 'Other',
        type: ['event'],
      },
      {
        confidence: 0.7144248485565186,
        end_index: 16,
        sct_code: '420227002',
        sct_term: 'Recommendation to',
        similarity: 1.0,
        start_index: 10,
        status: 'Other',
        type: ['procedure'],
      },
    ],
    text: '11\tTravel advice',
  },
  {
    mapped_info: [
      {
        confidence: 0.9998747110366821,
        end_index: 22,
        sct_code: '78737005',
        sct_term: 'Frontal sinusitis',
        similarity: 1.0,
        start_index: 4,
        status: 'Affirmed',
        type: ['disorder'],
      },
    ],
    text: '12\t"Sinusitis, frontal"',
  },
  {
    mapped_info: [
      {
        confidence: 0.9961812496185303,
        end_index: 22,
        sct_code: '238751002',
        sct_term: 'Perioral dermatitis',
        similarity: 1.0,
        start_index: 3,
        status: 'Affirmed',
        type: ['disorder'],
      },
    ],
    text: '13\tPerioral dermatitis',
  },
  {
    mapped_info: [
      {
        confidence: 0.6568598747253418,
        end_index: 27,
        sct_code: '14734007',
        sct_term: 'Administrative procedure',
        similarity: 1.0,
        start_index: 3,
        status: 'Other',
        type: ['procedure'],
      },
    ],
    text: '14\tAdministrative procedure',
  },
  {
    mapped_info: [
      {
        confidence: 0.8184093236923218,
        end_index: 15,
        sct_code: '16076005',
        sct_term: 'Prescription',
        similarity: 0.99,
        start_index: 3,
        status: 'Other',
        type: ['procedure'],
      },
    ],
    text: '15\tPrescription',
  },
  {
    mapped_info: [
      {
        confidence: 0.5534687638282776,
        end_index: 19,
        sct_code: '82127005',
        sct_term: 'Perianal abscess',
        similarity: 1.0,
        start_index: 3,
        status: 'Other',
        type: ['disorder'],
      },
    ],
    text: '16\tPerianal abscess',
  },
  {
    mapped_info: [
      {
        confidence: 0.9346798062324524,
        end_index: 24,
        sct_code: '160357008',
        sct_term: 'Family history: Hypertension',
        similarity: 1.0,
        start_index: 12,
        status: 'Affirmed',
        type: ['situation'],
      },
      {
        confidence: 0.6119537353515625,
        end_index: 11,
        sct_code: '2931005',
        sct_term: 'Probable diagnosis (contextual qualifier)',
        similarity: 1.0,
        start_index: 3,
        status: 'Affirmed',
        type: ['qualifier value'],
      },
    ],
    text: '17\tProbable Hypertension - Borderline',
  },
  {
    mapped_info: [
      {
        confidence: 0.998891294002533,
        end_index: 9,
        sct_code: '420008001',
        sct_term: 'Travel',
        similarity: 1.0,
        start_index: 3,
        status: 'Other',
        type: ['event'],
      },
      {
        confidence: 0.9917349815368652,
        end_index: 21,
        sct_code: '33879002',
        sct_term: 'Administration of vaccine to produce active immunity',
        similarity: 1.0,
        start_index: 10,
        status: 'Other',
        type: ['procedure'],
      },
    ],
    text: '18\tTravel vaccination',
  },
  {
    mapped_info: [
      {
        confidence: 0.9996285438537598,
        end_index: 9,
        sct_code: '49727002',
        sct_term: 'Cough',
        similarity: 0.99,
        start_index: 4,
        status: 'Affirmed',
        type: ['finding'],
      },
    ],
    text: '19\t"Cough, post infective"',
  },
  {
    mapped_info: [],
    text: '20\tSTI screen',
  },
];

// all tasks
export const allMappingTasks = [
  {
    id: '47',
    status: 'pending',
    num: 8,
    create_by: 'Vlada',
    create_at: '2003-12-15 15:17:17',
    update_at: '',
  },
  {
    id: '52',
    status: 'success',
    num: 25,
    create_by: 'Henry',
    create_at: '1981-04-26 06:12:29',
    update_at: '2007-09-20 23:51:33',
  },
  {
    id: '35',
    status: 'fail',
    num: 58,
    create_by: 'Susan',
    create_at: '1978-03-07 15:46:58',
    update_at: '',
  },
  {
    id: '25',
    status: 'success',
    num: 10,
    create_by: 'Susan',
    create_at: '2015-12-17 00:21:47',
    update_at: '1995-01-16 13:10:39',
  },
  {
    id: '26',
    status: 'success',
    num: 10,
    create_by: 'Susan',
    create_at: '2015-12-17 00:21:47',
    update_at: '1995-01-16 13:10:39',
  },
  {
    id: '27',
    status: 'success',
    num: 10,
    create_by: 'Susan',
    create_at: '2015-12-17 00:21:47',
    update_at: '1995-01-16 13:10:39',
  },
  {
    id: '28',
    status: 'success',
    num: 10,
    create_by: 'Susan',
    create_at: '2015-12-17 00:21:47',
    update_at: '1995-01-16 13:10:39',
  },
  {
    id: '29',
    status: 'success',
    num: 10,
    create_by: 'Susan',
    create_at: '2015-12-17 00:21:47',
    update_at: '1995-01-16 13:10:39',
  },
];

export const codeSystemGroups = [
  {
    concepts: [
      {
        description: 'd1',
        name: 'name1',
      },
      {
        description: 'd2',
        name: 'name2',
      },
      {
        description: 'd2',
        name: 'name3',
      },
      {
        description: 'd2',
        name: 'name4',
      },
      {
        description: 'd2',
        name: 'name5',
      },
      {
        description: 'd2',
        name: 'name6',
      },
      {
        description: 'd2',
        name: 'name7',
      },
    ],
    group: 'Bone',
    group_id: '1',
  },
  {
    concepts: [
      {
        description: 'd1',
        name: 'name1',
      },
      {
        description: 'd2',
        name: 'name2',
      },
    ],
    group: 'Heart',
    group_id: '2',
  },
  {
    concepts: [
      {
        description: 'd1',
        name: 'name4',
      },
      {
        description: 'd2',
        name: 'name5',
      },
    ],
    group: 'Lung',
    group_id: '3',
  },
];
