import { motion } from 'framer-motion'
import { ArrowDownCircle, ArrowUpCircle } from 'lucide-react'

const HEALTH_COLORS = {
  Excellent: '#34D399',
  Healthy: '#2DD4BF',
  Moderate: '#FBBF24',
  Degraded: '#FB923C',
  Critical: '#F87171',
}

export default function BatteryVisual({ soh = 0, health = 'Healthy', current = 0 }) {
  const color = HEALTH_COLORS[health] || '#2DD4BF'
  const fillPct = Math.max(4, Math.min(100, soh))
  const charging = current < 0.02 // heuristic: near-zero net draw reads as "idle/charging" in this demo

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative flex h-40 w-20 items-end justify-center">
        {/* battery terminal nub */}
        <div className="absolute -top-3 h-3 w-8 rounded-t-md bg-white/15" />

        {/* battery shell */}
        <div
          className="relative h-full w-full overflow-hidden rounded-2xl border-2"
          style={{ borderColor: 'rgba(255,255,255,0.14)' }}
        >
          <div className="absolute inset-0 bg-white/[0.02]" />
          {/* liquid fill */}
          <motion.div
            initial={{ height: '4%' }}
            animate={{ height: `${fillPct}%` }}
            transition={{ duration: 1.2, ease: 'easeOut' }}
            className="absolute bottom-0 left-0 right-0"
            style={{
              background: `linear-gradient(180deg, ${color}CC 0%, ${color}66 100%)`,
              boxShadow: `0 0 24px 2px ${color}55 inset`,
            }}
          >
            <motion.div
              className="absolute -top-1 left-0 right-0 h-2 opacity-70"
              style={{ background: color }}
              animate={{ opacity: [0.4, 0.9, 0.4] }}
              transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut' }}
            />
          </motion.div>
        </div>
      </div>

      <div className="flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.03] px-3 py-1">
        {charging ? (
          <ArrowUpCircle className="h-3.5 w-3.5 text-battery-healthy" />
        ) : (
          <ArrowDownCircle className="h-3.5 w-3.5 text-battery-moderate" />
        )}
        <span className="font-mono text-[11px] text-white/60">
          {charging ? 'Idle / trickle' : 'Discharging'}
        </span>
      </div>
    </div>
  )
}
