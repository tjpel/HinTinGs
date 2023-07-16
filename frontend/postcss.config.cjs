module.exports = {
    plugins: {
      tailwindcss: {
        content: [
          "./index.html",
          "./src/**/*.{js,ts,jsx,tsx}",
        ],
        theme: {
          extend: {},
        },
        plugins: [],
      },
      autoprefixer: {},
    }
  }