import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // background: "var(--background)",
        // foreground: "var(--foreground)",
        primary: "#6366F1", // Indigo
        secondary: "#F59E0B", // Amber
        background: "#F3F4F6", // Gray-100
        text: "#1F2937", // Gray-900
      },
    },
  },
  plugins: [],
} satisfies Config;
