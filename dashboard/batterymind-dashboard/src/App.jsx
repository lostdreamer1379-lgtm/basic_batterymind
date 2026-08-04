import { motion } from 'framer-motion'
import BackgroundFX from './components/BackgroundFX'
import Header from './components/Header'
import SOHGauge from './components/SOHGauge'
import BatteryVisual from './components/BatteryVisual'
import StatusCards from './components/StatusCards'
import LiveCharts from './components/LiveCharts'
import ShapPanel from './components/ShapPanel'
import RecommendationPanel from './components/RecommendationPanel'
import { useBatteryPolling } from './hooks/usePolling'

export default function App() {
  const { data, connected } = useBatteryPolling(1500)

  const status = data?.status
  const prediction = data?.prediction
  const reading = data?.reading
  const history = data?.history ?? []
  const explanation = data?.explainability
  const recommendations = data?.recommendations ?? []

  return (
    <div className="relative min-h-screen font-body">
      <BackgroundFX />

      <div className="relative z-10 mx-auto max-w-7xl px-5 py-8 sm:px-8 lg:px-10">
        <Header connected={connected} />

        {!connected && (
          <StatusBanner text="Backend not reachable at 127.0.0.1:5000 — start `python backend/app.py`." tone="critical" />
        )}
        {connected && status === 'no_data' && (
          <StatusBanner text="Connected, but no telemetry yet — start the simulator or connect Arduino." tone="idle" />
        )}
        {connected && status === 'warming_up' && (
          <StatusBanner text={data?.message || 'Collecting initial samples…'} tone="idle" />
        )}

        {/* Hero: SOH gauge + battery visual + status cards */}
        <motion.section
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="glass-card mt-6 rounded-3xl p-6 shadow-card sm:p-8"
        >
          <div className="flex flex-col items-center gap-8 lg:flex-row lg:items-stretch lg:justify-between">
            <div className="flex items-center justify-center">
              <SOHGauge
                soh={prediction?.soh ?? 0}
                health={prediction?.health ?? 'Healthy'}
                confidence={prediction?.confidence}
              />
            </div>
            <div className="flex items-center justify-center">
              <BatteryVisual
                soh={prediction?.soh ?? 0}
                health={prediction?.health ?? 'Healthy'}
                current={reading?.current ?? 0}
              />
            </div>
            <div className="flex-1">
              <StatusCards reading={reading} health={prediction?.health} risk={prediction?.risk} />
            </div>
          </div>
        </motion.section>

        {/* Live monitoring */}
        <section className="mt-8">
          <SectionLabel text="Live Monitoring" />
          <LiveCharts history={history} />
        </section>

        {/* Explainable AI + Recommendations */}
        <section className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div>
            <SectionLabel text="AI Intelligence & Explainability" />
            <ShapPanel explanation={explanation} />
          </div>
          <div>
            <SectionLabel text="Recommendation Engine" />
            <RecommendationPanel recommendations={recommendations} />
          </div>
        </section>

        <footer className="mt-10 pb-6 text-center text-[11px] uppercase tracking-[0.2em] text-white/25">
          Sense · Analyze · Explain · Recommend · Visualize
        </footer>
      </div>
    </div>
  )
}

function SectionLabel({ text }) {
  return (
    <div className="mb-3 flex items-center gap-3">
      <h2 className="font-display text-xs font-semibold uppercase tracking-[0.25em] text-white/40">{text}</h2>
      <div className="h-px flex-1 bg-gradient-to-r from-white/10 to-transparent" />
    </div>
  )
}

function StatusBanner({ text, tone }) {
  const toneStyles =
    tone === 'critical'
      ? 'border-battery-critical/30 bg-battery-critical/10 text-battery-critical'
      : 'border-battery-moderate/30 bg-battery-moderate/10 text-battery-moderate'
  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`mt-4 rounded-xl border px-4 py-2.5 text-sm ${toneStyles}`}
    >
      {text}
    </motion.div>
  )
}
