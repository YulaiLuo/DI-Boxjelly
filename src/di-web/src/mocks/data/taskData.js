export const mapTaskDetail = {
  id: '123456',
  userTeamId: '123456',
  status: 1,
  createdAt: '2023-05-03',
  updatedAt: null,
  totalNumber: 3,
  numberOfSuccess: 2,
  numberOfFail: 1,
  mappedItems: [
    {
      id: '1',
      mappingStatus: 1,
      originalText: 'Sinusitis',
      mappedText: 'Sinusitis',
      confidence: 0.87,
      source: {
        status: 0,
        snomed: {
          code: '122424',
          name: 'Sinusitis',
        },
        uil: null,
      },
      curate: null,
    },
    {
      id: '2',
      mappingStatus: 0,
      originalText: '????',
      mappedText: null,
      confidence: null,
      source: null,
      curate: null,
    },
    {
      id: '3',
      mappingStatus: 1,
      originalText: 'adfdf',
      mappedText: 'A uil term',
      confidence: 1,
      source: {
        status: 1,
        snomed: {
          id: '23',
          snomedCode: '122424',
          name: 'a snomed term',
        },
        uil: null,
      },
      curate: null,
    },
  ],
};
