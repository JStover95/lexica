/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,tsx}"],
  theme: {
    extend: {
      borderRadius: {
        '4xl': '2rem',
      }
    },
    colors: {
      "white": "#FFFFFF",
      "black": "#000000",
      "primary": "#008800"
    }
  },
  plugins: [],
}
