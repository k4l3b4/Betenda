const { colors } = require('@mui/material');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx}',
    './src/components/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: "class",
  theme: {
    extend: {
      fontSize: {
        "text-base": "12px"
      },
      colors: {
        main: "#1C8EC2",

        bgLight: "#E6E6E6",
        fgLight: "#FFFFFF",

        bgDark: "#858585",
        fgDark: "#2A2B2E",

      }
    },
  },
  plugins: [],
}
