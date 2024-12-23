const CracoAlias = require('craco-alias');

module.exports = {
  plugins: [
    {
      plugin: CracoAlias,
      options: {
        baseUrl: 'src',
        source: 'options',
        aliases: {
          '@': '.',
        },
      },
    },
    {
      plugin: require('craco-less'),
      // options: {
      //   noIeCompat: true,
      // },
    },
  ],
};
