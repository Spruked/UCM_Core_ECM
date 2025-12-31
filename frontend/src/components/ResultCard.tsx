import React from 'react'

const ResultCard: React.FC<{ data?: any }> = ({ data }) => {
  if (!data) return null

  const finalVerdict = data.final_verdict || {}
  const status = finalVerdict.status || 'UNKNOWN'
  const confidence = Math.round((data.confidence || finalVerdict.confidence || 0) * 100)
  const philosopherVerdicts = data.all_philosopher_verdicts || {}
  const metaAnalysis = data.meta_analysis || {}

  return (
    <div style={{ border: '1px solid #e6e6e6', padding: 16, borderRadius: 8, marginTop: 16 }}>
      <div style={{ fontSize: 18, fontWeight: 600 }}>Verdict: {status}</div>
      <div style={{ marginTop: 8 }}>
        <div style={{ height: 12, background: '#eee', borderRadius: 6, overflow: 'hidden' }}>
          <div style={{ width: `${confidence}%`, height: '100%', background: '#4caf50' }} />
        </div>
      </div>
      <div style={{ marginTop: 8, color: '#666' }}>Confidence: {confidence}%</div>
      
      {Object.keys(philosopherVerdicts).length > 0 && (
        <div style={{ marginTop: 16 }}>
          <h4>Philosopher Verdicts:</h4>
          <ul>
            {Object.entries(philosopherVerdicts).map(([skg, verdict]: [string, any]) => (
              <li key={skg}>
                <strong>{skg}:</strong> {verdict.status || 'UNKNOWN'} (conf: {Math.round((verdict.confidence || 0) * 100)}%)
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {metaAnalysis.softmax_advisory && (
        <div style={{ marginTop: 16 }}>
          <h4>Meta Analysis:</h4>
          <p>Epistemic Inevitability: {Math.round((metaAnalysis.softmax_advisory.epistemic_inevitability || 0) * 100)}%</p>
        </div>
      )}
    </div>
  )
}

export default ResultCard
