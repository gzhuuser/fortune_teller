/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      gridTemplateRows: {
        '8': 'repeat(8, minmax(0, 1fr)',
        'layout': '200px minmax(900px, 1fr) 100px',
      },
    },
  },
  plugins: [],
}

