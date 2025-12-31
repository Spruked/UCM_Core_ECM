import React, { useState } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const API_KEY = import.meta.env.VITE_API_KEY

const QueryForm: React.FC<{ onResult?: (r: any) => void }> = ({ onResult }) => {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null
    setSelectedFile(file)
    if (file) {
      const reader = new FileReader()
      reader.onload = (ev) => {
        const text = ev.target?.result as string
        setQuery(text)
      }
      reader.readAsText(file)
    }
  }

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query) return
    setLoading(true)
    try {
      const headers: any = {}
      if (API_KEY) {
        headers.Authorization = `Bearer ${API_KEY}`
      }
      const resp = await axios.post(`${API_BASE}/api/adjudicate`, { query }, { headers })
      setResult(resp.data)
      if (onResult) onResult(resp.data)
    } catch (err: any) {
      setResult({ error: err?.response?.data || err.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={submit}>
      <textarea
        placeholder="Enter your query..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: '100%', minHeight: 120, padding: 12, fontSize: 16 }}
      />
      <div style={{ marginTop: 12 }}>
        <input
          type="file"
          accept=".txt,.md,.json"
          onChange={handleFileChange}
          style={{ marginBottom: 12 }}
        />
        <button type="submit" disabled={loading} style={{ padding: '10px 18px' }}>
          {loading ? 'Adjudicating…' : 'Adjudicate'}
        </button>
      </div>
    </form>
  )
}

export default QueryForm
