/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  media: false, // or 'media' or 'class'
  theme: {
    extend: {
      zIndex: {
        "-10": "-10",
        "-20": "-20",
        "-30": "-30",
        "-40": "-40",
        "-50": "-50",
      },
    },
    fontFamily: {
      poppins: "Poppins, sans-serif",
      lato: "Lato, sans-serif",
    },
    screens: {
      "2xl-min": { min: "1536px" },
      "2xl": { max: "1535px" },

      xl: { max: "1279px" },

      "lg-min": { min: "1024px" },
      lg: { max: "1023px" },

      "md-min": { min: "801px" },
      md: { max: "800px" },

      "sm-min": { min: "640px" },
      sm: { max: "639px" },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
