import React from 'react'
import QueryForm from './components/QueryForm'
import { useState } from 'react'
import ResultCard from './components/ResultCard'

const App: React.FC = () => {
  const [lastResult, setLastResult] = useState<any | null>(null)

  return (
    <div style={{ maxWidth: 900, margin: '40px auto', fontFamily: 'Inter, system-ui, sans-serif' }}>
      <h1>UCM Core ECM — Frontend Demo</h1>
      <QueryForm onResult={(r: any) => setLastResult(r)} />
      <div style={{ marginTop: 24 }}>
        <ResultCard data={lastResult} />
      </div>
    </div>
  )
}

export default App
