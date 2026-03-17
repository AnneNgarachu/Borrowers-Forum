/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'navy': {
          900: '#1e3a5f',
          800: '#243b53',
          700: '#334e68',
          600: '#486581',
        },
        'gold': {
          500: '#f59e0b',
          400: '#fbbf24',
          100: '#fef3c7',
        },
      },
    },
  },
  plugins: [],
}