import { motion } from 'framer-motion'

const HEALTH_COLORS = {
  Excellent: '#34D399',
  Healthy: '#2DD4BF',
  Moderate: '#FBBF24',
  Degraded: '#FB923C',
  Critical: '#F87171',
}

export default function SOHGauge({ soh = 0, health = 'Healthy', confidence }) {
  const color = HEALTH_COLORS[health] || '#2DD4BF'
  const radius = 84
  const stroke = 12
  const circumference = 2 * Math.PI * radius
  const progress = Math.max(0, Math.min(100, soh)) / 100
  const dashOffset = circumference * (1 - progress)

  return (
    <div className="relative flex flex-col items-center justify-center">
      <svg width="220" height="220" viewBox="0 0 220 220" className="-rotate-90">
        <circle
          cx="110"
          cy="110"
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.06)"
          strokeWidth={stroke}
        />
        <motion.circle
          cx="110"
          cy="110"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: dashOffset }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
          style={{ filter: `drop-shadow(0 0 10px ${color}99)` }}
        />
      </svg>

      <div className="absolute flex flex-col items-center">
        <motion.span
          key={soh}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          className="font-display font-mono text-5xl font-semibold tabular-nums text-white"
        >
          {soh.toFixed(1)}
          <span className="text-xl text-white/40">%</span>
        </motion.span>
        <span className="mt-1 text-[11px] uppercase tracking-[0.2em] text-white/40">
          State of Health
        </span>
        {confidence != null && (
          <span className="mt-2 rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-0.5 font-mono text-[10px] text-white/50">
            {confidence.toFixed(1)}% model confidence
          </span>
        )}
      </div>
    </div>
  )
}
