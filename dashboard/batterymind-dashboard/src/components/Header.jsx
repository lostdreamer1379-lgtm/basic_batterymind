import { motion } from 'framer-motion'
import { Cpu, Wifi, WifiOff } from 'lucide-react'

export default function Header({ connected }) {
  return (
    <motion.header
      initial={{ opacity: 0, y: -16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
    >
      <div className="flex items-center gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-cyan-glow/25 bg-cyan-glow/10 shadow-glow-sm">
          <Cpu className="h-5 w-5 text-cyan-glow" strokeWidth={1.75} />
        </div>
        <div>
          <h1 className="font-display text-2xl font-semibold tracking-tight text-white sm:text-3xl">
            Battery<span className="text-cyan-glow">Mind</span>
          </h1>
          <p className="text-xs uppercase tracking-[0.2em] text-white/40">
            Explainable AI · IoT Battery Health Intelligence
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2 self-start rounded-full border border-white/10 bg-white/[0.03] px-4 py-2 sm:self-auto">
        {connected ? (
          <>
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-battery-healthy opacity-60" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-battery-healthy" />
            </span>
            <Wifi className="h-3.5 w-3.5 text-battery-healthy" />
            <span className="text-xs font-medium text-white/70">Live telemetry connected</span>
          </>
        ) : (
          <>
            <span className="h-2 w-2 rounded-full bg-battery-critical" />
            <WifiOff className="h-3.5 w-3.5 text-battery-critical" />
            <span className="text-xs font-medium text-white/50">Waiting for backend…</span>
          </>
        )}
      </div>
    </motion.header>
  )
}
