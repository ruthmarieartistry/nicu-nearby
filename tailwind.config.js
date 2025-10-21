/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        "alcea-ruby": "#7d2431",
        "alcea-green": "#217045",
        "alcea-mustard": "#e1b321",
        "alcea-brown": "#a5630b",
        "alcea-teal": "#005567",
      },
    },
  },
  plugins: [],
};
