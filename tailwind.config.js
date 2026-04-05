/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './docs/index.html',
    './networking/index.html',
    './features/**/*.html',
    './use-cases/**/*.html',
    './src/**/*.{css,js}',
  ],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: '#0d1117',
          raised: '#151d28',
          border: '#30363d',
        },
        accent: {
          DEFAULT: '#22c55e',
          light: '#4ade80',
        },
        muted: '#8b949e',
      },
      fontFamily: {
        mono: ['"Source Code Pro"', 'monospace'],
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
