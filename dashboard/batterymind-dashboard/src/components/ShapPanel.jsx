import { motion } from 'framer-motion'
import { BrainCircuit } from 'lucide-react'

const IMPACT_COLOR = {
  'High contribution': '#F87171',
  'Medium contribution': '#FBBF24',
  'Low contribution': '#2DD4BF',
}

function prettyFeatureName(name) {
  return name
    .split('_')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
}

export default function ShapPanel({ explanation }) {
  const factors = explanation?.top_factors ?? []
  const maxAbs = Math.max(...factors.map((f) => Math.abs(f.shap_value)), 0.001)

  return (
    <div className="glass-card rounded-2xl p-5 shadow-card">
      <div className="mb-1 flex items-center gap-2">
        <BrainCircuit className="h-4 w-4 text-cyan-glow" strokeWidth={1.75} />
        <h2 className="font-display text-sm font-semibold uppercase tracking-[0.15em] text-white/80">
          Explainable AI
        </h2>
      </div>
      <p className="mb-5 text-sm text-white/40">Why is battery health changing?</p>

      {factors.length === 0 ? (
        <p className="text-sm text-white/30">Waiting for enough samples to compute SHAP attributions…</p>
      ) : (
        <div className="space-y-4">
          {factors.map((f, i) => {
            const widthPct = (Math.abs(f.shap_value) / maxAbs) * 100
            const color = IMPACT_COLOR[f.impact] || '#2DD4BF'
            return (
              <motion.div
                key={f.feature}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4, delay: i * 0.05 }}
              >
                <div className="mb-1 flex items-baseline justify-between gap-2">
                  <span className="text-sm font-medium text-white/85">{prettyFeatureName(f.feature)}</span>
                  <span className="whitespace-nowrap font-mono text-[11px]" style={{ color }}>
                    {f.impact}
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-white/[0.05]">
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: color, boxShadow: `0 0 12px 0 ${color}88` }}
                    initial={{ width: 0 }}
                    animate={{ width: `${widthPct}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut', delay: i * 0.05 }}
                  />
                </div>
                <p className="mt-1.5 text-xs leading-relaxed text-white/40">
                  {f.meaning} — <span className="text-white/30">{f.direction}</span>
                </p>
              </motion.div>
            )
          })}
        </div>
      )}
    </div>
  )
}
