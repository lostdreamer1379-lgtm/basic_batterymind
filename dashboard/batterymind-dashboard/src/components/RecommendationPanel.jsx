import { motion } from 'framer-motion'
import {
  CheckCircle2,
  AlertTriangle,
  OctagonAlert,
  Thermometer,
  Zap,
  Activity,
  Gauge,
  BatteryCharging,
  ShieldAlert,
  ListChecks,
} from 'lucide-react'

const ICON_MAP = {
  'check-circle': CheckCircle2,
  'alert-triangle': AlertTriangle,
  'octagon-alert': OctagonAlert,
  thermometer: Thermometer,
  zap: Zap,
  activity: Activity,
  gauge: Gauge,
  'battery-charging': BatteryCharging,
  'shield-alert': ShieldAlert,
}

const PRIORITY_STYLES = {
  Low: 'text-battery-excellent bg-battery-excellent/10 border-battery-excellent/25',
  Medium: 'text-battery-moderate bg-battery-moderate/10 border-battery-moderate/25',
  High: 'text-battery-degraded bg-battery-degraded/10 border-battery-degraded/25',
  Critical: 'text-battery-critical bg-battery-critical/10 border-battery-critical/25',
}

export default function RecommendationPanel({ recommendations = [] }) {
  return (
    <div className="glass-card rounded-2xl p-5 shadow-card">
      <div className="mb-4 flex items-center gap-2">
        <ListChecks className="h-4 w-4 text-cyan-glow" strokeWidth={1.75} />
        <h2 className="font-display text-sm font-semibold uppercase tracking-[0.15em] text-white/80">
          Recommendations
        </h2>
      </div>

      {recommendations.length === 0 ? (
        <p className="text-sm text-white/30">No recommendations yet — waiting for a stable reading window.</p>
      ) : (
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {recommendations.map((rec, i) => {
            const Icon = ICON_MAP[rec.icon] || CheckCircle2
            return (
              <motion.div
                key={`${rec.title}-${i}`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: i * 0.06 }}
                className="rounded-xl border border-white/8 bg-white/[0.02] p-4"
              >
                <div className="mb-2 flex items-center justify-between">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-cyan-glow/10">
                    <Icon className="h-4 w-4 text-cyan-glow" strokeWidth={1.75} />
                  </div>
                  <span
                    className={`rounded-full border px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide ${
                      PRIORITY_STYLES[rec.priority] || PRIORITY_STYLES.Medium
                    }`}
                  >
                    {rec.priority}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-white/90">{rec.title}</h3>
                <p className="mt-1 text-xs leading-relaxed text-white/45">{rec.explanation}</p>
              </motion.div>
            )
          })}
        </div>
      )}
    </div>
  )
}
