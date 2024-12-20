const tailwindcss = require('tailwindcss');
const autoprefixer = require('autoprefixer');

module.exports = {
  plugins: [
    require('postcss-import'),
    tailwindcss('./tailwind.config.js'),
    autoprefixer,
  ]
};
