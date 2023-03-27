/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      textColor: {
        primary: '#074EE8',
      },
    },
  },
  plugins: [],
  corePlugins: {
    // Remove Tailwind CSS's preflight style so it can use the Ant Design's preflight instead (reset.css).
    preflight: false,
  },
};
