/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        void: {
          950: "#05070C",
          900: "#0A0E17",
          800: "#0F1420",
          700: "#161C2C",
          600: "#1E2638",
        },
        cyan: {
          glow: "#22D3EE",
        },
        battery: {
          excellent: "#34D399",
          healthy: "#2DD4BF",
          moderate: "#FBBF24",
          degraded: "#FB923C",
          critical: "#F87171",
        },
      },
      boxShadow: {
        glow: "0 0 40px -8px rgba(45, 212, 191, 0.45)",
        "glow-sm": "0 0 20px -6px rgba(45, 212, 191, 0.5)",
        card: "0 8px 32px 0 rgba(0, 0, 0, 0.45)",
      },
      backgroundImage: {
        "grid-pattern":
          "linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)",
        "radial-fade":
          "radial-gradient(60% 50% at 50% 0%, rgba(45,212,191,0.10) 0%, rgba(10,14,23,0) 70%)",
      },
      backgroundSize: {
        grid: "36px 36px",
      },
      animation: {
        "pulse-slow": "pulse 3.5s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        float: "float 6s ease-in-out infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-6px)" },
        },
      },
    },
  },
  plugins: [],
}
