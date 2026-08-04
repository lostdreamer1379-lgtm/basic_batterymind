import { motion } from 'framer-motion'
import { AreaChart, Area, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'

const CHART_DEFS = [
  { key: 'voltage', label: 'Voltage', unit: 'V', color: '#22D3EE', domain: [3.0, 4.3] },
  { key: 'current', label: 'Current', unit: 'A', color: '#2DD4BF', domain: [0, 2.5] },
  { key: 'temperature', label: 'Temperature', unit: '°C', color: '#FBBF24', domain: [15, 55] },
]

function ChartTooltip({ active, payload, unit }) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-lg border border-white/10 bg-void-800/95 px-3 py-2 font-mono text-xs text-white shadow-card">
      {payload[0].value?.toFixed(2)} {unit}
    </div>
  )
}

export default function LiveCharts({ history = [] }) {
  const chartData = history.map((h, i) => ({ index: i, ...h }))

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
      {CHART_DEFS.map((def, i) => (
        <motion.div
          key={def.key}
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 * i }}
          className="glass-card rounded-2xl p-4 shadow-card"
        >
          <div className="mb-2 flex items-center justify-between">
            <span className="text-xs font-medium uppercase tracking-[0.15em] text-white/50">
              {def.label} History
            </span>
            <span className="font-mono text-xs text-white/30">{def.unit}</span>
          </div>
          <div className="h-40">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id={`grad-${def.key}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={def.color} stopOpacity={0.45} />
                    <stop offset="100%" stopColor={def.color} stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="index" hide />
                <YAxis
                  domain={def.domain}
                  tick={{ fill: 'rgba(255,255,255,0.3)', fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                  width={32}
                />
                <Tooltip content={<ChartTooltip unit={def.unit} />} />
                <Area
                  type="monotone"
                  dataKey={def.key}
                  stroke={def.color}
                  strokeWidth={2}
                  fill={`url(#grad-${def.key})`}
                  isAnimationActive={true}
                  animationDuration={400}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      ))}
    </div>
  )
}
