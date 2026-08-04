import { useEffect, useRef, useState } from 'react'
import { fetchBatteryStatus } from '../api/client'

export function useBatteryPolling(intervalMs = 1500) {
  const [data, setData] = useState(null)
  const [connected, setConnected] = useState(false)
  const [error, setError] = useState(null)
  const timerRef = useRef(null)

  useEffect(() => {
    let cancelled = false

    async function tick() {
      try {
        const result = await fetchBatteryStatus()
        if (cancelled) return
        setData((previous) => {
          if (result.history.length > 0 || !result.reading) {
            return result
          }
          const previousHistory = previous?.history ?? []
          return {
            ...result,
            history: [...previousHistory, result.reading].slice(-60),
          }
        })
        setConnected(true)
        setError(null)
      } catch (err) {
        if (cancelled) return
        setConnected(false)
        setError(err.message)
      }
    }

    tick()
    timerRef.current = setInterval(tick, intervalMs)
    return () => {
      cancelled = true
      clearInterval(timerRef.current)
    }
  }, [intervalMs])

  return { data, connected, error }
}
