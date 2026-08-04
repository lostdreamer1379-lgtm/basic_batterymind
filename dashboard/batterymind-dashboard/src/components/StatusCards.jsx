import { motion } from 'framer-motion'
import { Zap, Activity, Thermometer, ShieldCheck, TrendingUp } from 'lucide-react'

const RISK_COLORS = {
  Low: 'text-battery-excellent border-battery-excellent/30 bg-battery-excellent/10',
  Medium: 'text-battery-moderate border-battery-moderate/30 bg-battery-moderate/10',
  High: 'text-battery-degraded border-battery-degraded/30 bg-battery-degraded/10',
  Critical: 'text-battery-critical border-battery-critical/30 bg-battery-critical/10',
}

const HEALTH_COLORS = {
  Excellent: 'text-battery-excellent border-battery-excellent/30 bg-battery-excellent/10',
  Healthy: 'text-battery-healthy border-battery-healthy/30 bg-battery-healthy/10',
  Moderate: 'text-battery-moderate border-battery-moderate/30 bg-battery-moderate/10',
  Degraded: 'text-battery-degraded border-battery-degraded/30 bg-battery-degraded/10',
  Critical: 'text-battery-critical border-battery-critical/30 bg-battery-critical/10',
}

function MetricCard({ icon: Icon, label, value, unit, delay }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className="glass-card rounded-2xl p-4 shadow-card"
    >
      <div className="flex items-center gap-2 text-white/40">
        <Icon className="h-3.5 w-3.5" strokeWidth={1.75} />
        <span className="text-[11px] uppercase tracking-[0.15em]">{label}</span>
      </div>
      <div className="mt-2 font-mono text-2xl font-medium tabular-nums text-white">
        {value}
        <span className="ml-1 text-sm text-white/40">{unit}</span>
      </div>
    </motion.div>
  )
}

export default function StatusCards({ reading, health, risk }) {
  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-5">
      <MetricCard icon={Activity} label="Voltage" value={reading?.voltage?.toFixed(2) ?? '—'} unit="V" delay={0.05} />
      <MetricCard icon={Zap} label="Current" value={reading?.current?.toFixed(2) ?? '—'} unit="A" delay={0.1} />
      <MetricCard icon={Thermometer} label="Temperature" value={reading?.temperature?.toFixed(1) ?? '—'} unit="°C" delay={0.15} />

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className={`glass-card flex flex-col justify-center rounded-2xl border p-4 shadow-card ${HEALTH_COLORS[health] || ''}`}
      >
        <div className="flex items-center gap-2 opacity-70">
          <ShieldCheck className="h-3.5 w-3.5" strokeWidth={1.75} />
          <span className="text-[11px] uppercase tracking-[0.15em]">Health</span>
        </div>
        <div className="mt-2 font-display text-xl font-semibold">{health || '—'}</div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.25 }}
        className={`glass-card flex flex-col justify-center rounded-2xl border p-4 shadow-card ${RISK_COLORS[risk] || ''}`}
      >
        <div className="flex items-center gap-2 opacity-70">
          <TrendingUp className="h-3.5 w-3.5" strokeWidth={1.75} />
          <span className="text-[11px] uppercase tracking-[0.15em]">Risk</span>
        </div>
        <div className="mt-2 font-display text-xl font-semibold">{risk || '—'}</div>
      </motion.div>
    </div>
  )
}
