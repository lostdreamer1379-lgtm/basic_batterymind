export default function BackgroundFX() {
  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden">
      {/* base grid */}
      <div className="absolute inset-0 bg-void-900 bg-grid-pattern bg-grid [mask-image:radial-gradient(ellipse_80%_60%_at_50%_0%,#000_40%,transparent_100%)]" />
      {/* top radial glow */}
      <div className="absolute inset-0 bg-radial-fade" />
      {/* ambient orbs */}
      <div className="absolute -top-32 left-1/4 h-[420px] w-[420px] rounded-full bg-cyan-glow/10 blur-[120px] animate-pulse-slow" />
      <div className="absolute top-1/3 right-0 h-[360px] w-[360px] rounded-full bg-battery-healthy/10 blur-[120px] animate-pulse-slow" />
      <div className="absolute bottom-0 left-0 h-[300px] w-[300px] rounded-full bg-battery-moderate/5 blur-[120px]" />
    </div>
  )
}
