const BASE_URL = 'http://127.0.0.1:5000'

function toImpactLabel(shapValue) {
  const absValue = Math.abs(Number(shapValue) || 0)
  if (absValue >= 0.05) return 'High contribution'
  if (absValue >= 0.02) return 'Medium contribution'
  return 'Low contribution'
}

function normalizePrediction(prediction = {}) {
  const rawSoh = Number(prediction.soh)
  const sohPercentage = Number(prediction.soh_percentage)
  const soh =
    Number.isFinite(sohPercentage)
      ? sohPercentage
      : Number.isFinite(rawSoh)
        ? (rawSoh <= 1 ? rawSoh * 100 : rawSoh)
        : 0

  return {
    ...prediction,
    soh,
  }
}

function normalizeExplanation(raw) {
  if (raw?.explainability?.top_factors) return raw.explainability
  const shap = Array.isArray(raw?.shap) ? raw.shap : []
  return {
    top_factors: shap.map((f) => {
      const shapValue = Number(f.shap_value ?? f.impact ?? 0)
      return {
        feature: f.feature,
        shap_value: shapValue,
        impact: typeof f.impact === 'string' ? f.impact : toImpactLabel(shapValue),
        direction: f.direction ?? (shapValue >= 0 ? 'Increase SOH' : 'Decrease SOH'),
        meaning: f.meaning ?? `Model contribution: ${shapValue.toFixed(4)}`,
      }
    }),
  }
}

function normalizeRecommendations(raw) {
  if (Array.isArray(raw?.recommendations)) return raw.recommendations

  const report = raw?.recommendation
  if (!report) return []

  const priority = report.risk || 'Medium'
  const general = (report.general_recommendations || []).map((text, index) => ({
    title: `General Guidance ${index + 1}`,
    explanation: text,
    icon: 'check-circle',
    priority,
  }))
  const shap = (report.shap_recommendations || []).map((text, index) => ({
    title: `Model-Driven Action ${index + 1}`,
    explanation: text,
    icon: 'activity',
    priority,
  }))

  return [...general, ...shap]
}

function normalizeStatus(status) {
  if (status === 'collecting' || status === 'Collecting') return 'warming_up'
  return status
}

function normalizeBatteryPayload(raw) {
  return {
    ...raw,
    status: normalizeStatus(raw?.status),
    reading: raw?.reading ?? raw?.sensor ?? null,
    prediction: normalizePrediction(raw?.prediction),
    explainability: normalizeExplanation(raw),
    recommendations: normalizeRecommendations(raw),
    history: Array.isArray(raw?.history) ? raw.history : [],
  }
}

export async function fetchBatteryStatus() {
  const res = await fetch(`${BASE_URL}/battery-status`, {
    cache: 'no-store',
  })
  if (!res.ok) {
    throw new Error(`Backend responded with ${res.status}`)
  }
  const payload = await res.json()
  return normalizeBatteryPayload(payload)
}
