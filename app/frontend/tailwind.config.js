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
      "primary": "#008800"
    }
  },
  plugins: [],
}
