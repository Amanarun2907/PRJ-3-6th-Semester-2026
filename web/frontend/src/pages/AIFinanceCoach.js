import React, { useState } from 'react';
import { ai } from '../api';
import PlotlyChart from '../components/PlotlyChart';

export default function AIFinanceCoach() {
  const [language,    setLanguage]    = useState('English');
  const [loading,     setLoading]     = useState(false);
  const [result,      setResult]      = useState(null);
  const [error,       setError]       = useState('');

  const explain = async () => {
    setLoading(true); setError(''); setResult(null);
    try {
      const r = await ai.explainLoss(language);
      if (r.data.error) { setError(r.data.error); }
      else { setResult(r.data); }
    } catch (e) { setError('Failed to fetch. Check backend connection.'); }
    finally { setLoading(false); }
  };

  const ps = result?.portfolio_summary;
  const holdings = result?.holdings || [];
  const sectorPerf = result?.sector_perf || {};
  const fiiDii = result?.fii_dii || {};

  const todayPnlBar = holdings.length ? [{
    type: 'bar', orientation: 'h',
    x: holdings.map(h => h.today_pnl),
    y: holdings.map(h => h.company_name || h.symbol),
    marker: { color: holdings.map(h => h.today_pnl >= 0 ? '#00ff88' : '#ff5252') },
    text: holdings.map(h => `₹${h.today_pnl?.toLocaleString('en-IN')}`),
    textposition: 'outside',
  }] : [];

  const todayPctBar = holdings.length ? [{
    type: 'bar',
    x: holdings.map(h => h.company_name || h.symbol),
    y: holdings.map(h => h.today_chg_pct),
    marker: { color: holdings.map(h => h.today_chg_pct >= 0 ? '#00ff88' : '#ff5252') },
    text: holdings.map(h => `${h.today_chg_pct > 0 ? '+' : ''}${h.today_chg_pct?.toFixed(2)}%`),
    textposition: 'outside',
  }] : [];

  const allocationPie = holdings.length ? [{
    type: 'pie',
    labels: holdings.map(h => h.company_name || h.symbol),
    values: holdings.map(h => h.curr_val),
    hole: 0.45,
    textinfo: 'label+percent',
    marker: { line: { color: '#0d1117', width: 2 } },
  }] : [];

  const overallBubble = holdings.length ? [{
    type: 'scatter', mode: 'markers+text',
    x: holdings.map(h => h.company_name || h.symbol),
    y: holdings.map(h => h.overall_pnl_pct),
    marker: {
      size: holdings.map(h => Math.max(12, Math.min(50, Math.abs(h.overall_pnl_pct) * 2 + 12))),
      color: holdings.map(h => h.overall_pnl_pct >= 0 ? '#00ff88' : '#ff5252'),
      line: { color: '#fff', width: 1 },
    },
    text: holdings.map(h => `${h.overall_pnl_pct > 0 ? '+' : ''}${h.overall_pnl_pct?.toFixed(1)}%`),
    textposition: 'top center',
  }] : [];

  const sectorBar = Object.keys(sectorPerf).length ? [{
    type: 'bar',
    x: Object.keys(sectorPerf),
    y: Object.values(sectorPerf),
    marker: { color: Object.values(sectorPerf).map(v => v >= 0 ? '#00ff88' : '#ff5252') },
    text: Object.values(sectorPerf).map(v => `${v > 0 ? '+' : ''}${v}%`),
    textposition: 'outside',
  }] : [];

  const fiiGauge = fiiDii.fii_net != null ? [{
    type: 'indicator', mode: 'gauge+number+delta',
    value: fiiDii.fii_net,
    delta: { reference: 0, increasing: { color: '#00ff88' }, decreasing: { color: '#ff5252' } },
    number: { suffix: ' Cr', font: { color: fiiDii.fii_net >= 0 ? '#00ff88' : '#ff5252' } },
    title: { text: 'FII Net Flow (₹ Cr)', font: { color: '#00d4ff' } },
    gauge: {
      axis: { range: [-5000, 5000] },
      bar: { color: fiiDii.fii_net >= 0 ? '#00ff88' : '#ff5252' },
      steps: [
        { range: [-5000,-1000], color: 'rgba(255,82,82,0.2)' },
        { range: [-1000, 1000], color: 'rgba(255,193,7,0.1)' },
        { range: [1000,  5000], color: 'rgba(0,255,136,0.2)' },
      ],
    },
  }] : [];

  const pnlColor = ps?.today_pnl >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';

  return (
    <div>
      <div className="section-title">🧠 AI Finance Coach — Explain My Portfolio</div>
      <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
        Live prices · NSE FII/DII · Sector performance · Google Finance news · Groq Llama 3.3 70B
      </div>

      {/* Controls */}
      <div className="card" style={{ marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', gap: 16, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div>
            <label>Response Language</label>
            <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
              {['English', 'Hindi'].map(l => (
                <button key={l} className={`btn ${language === l ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ padding: '6px 18px' }} onClick={() => setLanguage(l)}>{l}</button>
              ))}
            </div>
          </div>
          <button className="btn btn-primary" style={{ padding: '10px 28px', fontSize: '0.95rem' }}
            onClick={explain} disabled={loading}>
            {loading ? '⏳ Analysing your portfolio...' : `🤖 Explain My Portfolio in ${language}`}
          </button>
        </div>
        <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', marginTop: 8 }}>
          ⚠️ First add stocks in Portfolio & Risk Manager, then come here for AI explanation.
        </div>
      </div>

      {error && (
        <div style={{ background: 'rgba(255,82,82,0.1)', border: '1px solid var(--accent-red)',
          borderRadius: 10, padding: '1rem', marginBottom: '1.25rem', color: 'var(--accent-red)' }}>
          ❌ {error}
        </div>
      )}

      {result && (
        <>
          {/* KPIs */}
          <div className="grid-5" style={{ marginBottom: '1.25rem' }}>
            {[
              { label: "Today's P&L",   val: `₹${ps?.today_pnl?.toLocaleString('en-IN')}`,  sub: `${ps?.today_pct > 0 ? '+' : ''}${ps?.today_pct?.toFixed(2)}%`, color: pnlColor },
              { label: 'Overall P&L',   val: `₹${(ps?.total_current - ps?.total_invested)?.toLocaleString('en-IN')}`, sub: 'Since buy', color: (ps?.total_current - ps?.total_invested) >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' },
              { label: 'Current Value', val: `₹${ps?.total_current?.toLocaleString('en-IN')}`, sub: `Invested ₹${ps?.total_invested?.toLocaleString('en-IN')}`, color: 'var(--accent)' },
              { label: 'NIFTY 50',      val: result.nifty_chg != null ? `${result.nifty_chg > 0 ? '+' : ''}${result.nifty_chg}%` : 'N/A', sub: result.nifty_val?.toLocaleString('en-IN'), color: result.nifty_chg >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' },
              { label: 'FII Net Flow',  val: fiiDii.fii_net != null ? `₹${fiiDii.fii_net?.toLocaleString('en-IN')} Cr` : 'N/A', sub: fiiDii.date || '', color: fiiDii.fii_net >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' },
            ].map(k => (
              <div key={k.label} className="kpi-card" style={{ borderLeftColor: k.color }}>
                <div className="kpi-label">{k.label}</div>
                <div className="kpi-value" style={{ color: k.color, fontSize: '1.1rem' }}>{k.val}</div>
                <div className="kpi-sub">{k.sub}</div>
              </div>
            ))}
          </div>

          {/* Charts row 1 */}
          <div className="grid-2" style={{ marginBottom: '1rem' }}>
            <div className="card">
              <PlotlyChart data={todayPnlBar}
                layout={{ title: "Today's P&L per Stock (₹)", height: 350,
                  xaxis: { title: '₹ P&L', tickformat: ',.0f' },
                  shapes: [{ type:'line', y0:-0.5, y1:holdings.length-0.5, x0:0, x1:0, line:{color:'#555',dash:'dash'} }] }}/>
            </div>
            <div className="card">
              <PlotlyChart data={todayPctBar}
                layout={{ title: "Today's % Change per Stock", height: 350,
                  yaxis: { title: '% Change' },
                  shapes: [{ type:'line', x0:-0.5, x1:holdings.length-0.5, y0:0, y1:0, line:{color:'#555',dash:'dash'} }] }}/>
            </div>
          </div>

          {/* Charts row 2 */}
          <div className="grid-2" style={{ marginBottom: '1rem' }}>
            <div className="card">
              <PlotlyChart data={allocationPie}
                layout={{ title: 'Portfolio Allocation (Current Value)', height: 380, showlegend: true }}/>
            </div>
            <div className="card">
              <PlotlyChart data={overallBubble}
                layout={{ title: 'Overall P&L % Since Buy', height: 380,
                  yaxis: { title: 'Overall P&L %' },
                  shapes: [{ type:'line', x0:-0.5, x1:holdings.length-0.5, y0:0, y1:0, line:{color:'#555',dash:'dash'} }] }}/>
            </div>
          </div>

          {/* Charts row 3 */}
          <div className="grid-2" style={{ marginBottom: '1rem' }}>
            <div className="card">
              {sectorBar.length > 0
                ? <PlotlyChart data={sectorBar}
                    layout={{ title: 'Live Sector Performance Today (%)', height: 320,
                      yaxis: { title: '% Change' },
                      shapes: [{ type:'line', x0:-0.5, x1:Object.keys(sectorPerf).length-0.5, y0:0, y1:0, line:{color:'#555',dash:'dash'} }] }}/>
                : <div style={{ color:'var(--text-secondary)', padding:'2rem', textAlign:'center' }}>Sector data unavailable</div>
              }
            </div>
            <div className="card">
              {fiiGauge.length > 0
                ? <PlotlyChart data={fiiGauge} layout={{ height: 320 }}/>
                : <div style={{ color:'var(--text-secondary)', padding:'2rem', textAlign:'center' }}>FII/DII data unavailable</div>
              }
            </div>
          </div>

          {/* AI Explanation */}
          <div className="card" style={{ borderLeft: `4px solid ${pnlColor}`, marginBottom: '1rem' }}>
            <div style={{ fontWeight: 700, color: pnlColor, marginBottom: '0.75rem', fontSize: '1rem' }}>
              {ps?.today_pnl >= 0 ? '📈' : '📉'} AI Analysis — {new Date().toLocaleString('en-IN')}
            </div>
            <div style={{ color: 'var(--text-primary)', lineHeight: 1.9, whiteSpace: 'pre-wrap', fontSize: '0.9rem' }}>
              {result.explanation}
            </div>
          </div>

          {/* News used */}
          {result.headlines?.length > 0 && (
            <details className="card">
              <summary style={{ cursor: 'pointer', color: 'var(--accent)', fontWeight: 600 }}>
                📰 Live News Headlines Used for Analysis
              </summary>
              <div style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: 6 }}>
                {result.headlines.map((h, i) => (
                  <div key={i} style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', paddingLeft: 8,
                    borderLeft: '2px solid var(--border)' }}>{i+1}. {h}</div>
                ))}
              </div>
            </details>
          )}
        </>
      )}
    </div>
  );
}
