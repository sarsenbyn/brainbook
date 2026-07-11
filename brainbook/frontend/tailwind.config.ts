/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Здесь можно добавлять свои цвета, шрифты и т.д.
      colors: {
        'ait-blue': '#1e40af', // пример: твой фирменный цвет
      }
    },
  },
  plugins: [],
}