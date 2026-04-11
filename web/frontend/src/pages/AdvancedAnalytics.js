import React, { useEffect, useState } from 'react';
import { analytics } from '../api';
import PlotlyChart from '../components/PlotlyChart';

export default function AdvancedAnalytics() {
  const [heatmap,  setHeatmap]  = useState(null);
  const [corr,     setCorr]     = useState(null);
  const [volume,   setVolume]   = useState([]);
  const [breadth,  setBreadth]  = useState(null);
  const [loading,  setLoading]  = useState(true);
  const [tab,      setTab]      = useState('heatmap');
  const [corrPeriod, setCorrPeriod] = useState('3mo');

  const load = () => {
    setLoading(true);
    Promise.all([
      analytics.sectorHeatmap(),
      analytics.correlation(corrPeriod),
      analytics.volumeAnalysis(),
      analytics.marketBreadth(),
    ]).then(([h, c, v, b]) => {
      setHeatmap(h.data); setCorr(c.data); setVolume(v.data); setBreadth(b.data);
    }).catch(console.error).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [corrPeriod]);

  const heatmapChart = heatmap?.sectors ? [{
    type: 'bar',
    x: Object.keys(heatmap.sectors),
    y: Object.values(heatmap.sectors),
    marker: { color: Object.values(heatmap.sectors).map(v => v >= 0 ? '#00ff88' : '#ff5252') },
    text: Object.values(heatmap.sectors).map(v => `${v > 0 ? '+' : ''}${v}%`),
    textposition: 'outside',
  }] : [];

  const corrChart = corr?.matrix ? [{
    type: 'heatmap',
    z: corr.matrix,
    x: corr.stocks,
    y: corr.stocks,
    colorscale: [[0,'#ff5252'],[0.5,'#ffc107'],[1,'#00ff88']],
    zmid: 0,
    text: corr.matrix.map(row => row.map(v => v?.toFixed(2))),
    texttemplate: '%{text}',
    textfont: { size: 10 },
    colorbar: { title: 'Correlation' },
  }] : [];

  const volBar = volume.length ? [{
    type: 'bar',
    x: volume.map(v => v.symbol),
    y: volume.map(v => v.vol_ratio),
    marker: { color: volume.map(v => v.vol_ratio > 1.5 ? '#ff5252' : '#00d4ff') },
    text: volume.map(v => `${v.vol_ratio}x`),
    textposition: 'outside',
  }] : [];

  const breadthGauge = breadth ? [{
    type: 'indicator', mode: 'gauge+number+delta',
    value: breadth.strength,
    delta: { reference: 50, increasing: { color: '#00ff88' }, decreasing: { color: '#ff5252' } },
    number: { suffix: '%', font: { color: breadth.strength > 60 ? '#00ff88' : breadth.strength < 40 ? '#ff5252' : '#ffc107' } },
    title: { text: `Market Breadth Strength — ${breadth.sentiment}`, font: { color: '#00d4ff' } },
    gauge: {
      axis: { range: [0, 100] },
      bar: { color: breadth.strength > 60 ? '#00ff88' : breadth.strength < 40 ? '#ff5252' : '#ffc107' },
      steps: [
        { range: [0,  33], color: 'rgba(255,82,82,0.2)' },
        { range: [33, 67], color: 'rgba(255,193,7,0.1)' },
        { range: [67,100], color: 'rgba(0,255,136,0.2)' },
      ],
    },
  }] : [];

  return (
    <div>
      <div className="section-title">📈 Advanced Analytics</div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
          Live sector data · Correlation matrix · Volume intelligence · Market breadth
        </div>
        <button className="btn btn-secondary" style={{ fontSize: '0.78rem' }} onClick={load}>🔄 Refresh</button>
      </div>

      <div className="tab-bar">
        {[
          ['heatmap','🔥 Sector Heatmap'],
          ['correlation','🔗 Correlation'],
          ['volume','📊 Volume'],
          ['breadth','⚡ Breadth'],
        ].map(([id,label])=>(
          <button key={id} className={`tab ${tab===id?'active':''}`} onClick={()=>setTab(id)}>{label}</button>
        ))}
      </div>

      {loading && <div className="loading"><div className="spinner"/><span>Fetching live analytics...</span></div>}

      {tab === 'heatmap' && !loading && heatmapChart.length > 0 && (
        <div>
          <div className="card" style={{ marginBottom: '1rem' }}>
            <PlotlyChart data={heatmapChart}
              layout={{ title: 'Live Sector Performance Today (%)', height: 420,
                yaxis: { title: '% Change' },
                shapes: [{ type:'line', x0:-0.5, x1:Object.keys(heatmap.sectors).length-0.5, y0:0, y1:0, line:{color:'#555',dash:'dash'} }] }}/>
          </div>
          <div className="grid-4">
            {Object.entries(heatmap.sectors).sort((a,b)=>b[1]-a[1]).map(([s,v])=>{
              const c = v >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
              return (
                <div key={s} className="card" style={{ borderLeft:`3px solid ${c}`, textAlign:'center' }}>
                  <div style={{ fontWeight:600, color:'var(--accent)' }}>{s}</div>
                  <div style={{ fontSize:'1.3rem', fontWeight:800, color:c, marginTop:4 }}>
                    {v > 0 ? '+' : ''}{v}%
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {tab === 'correlation' && !loading && (
        <div>
          <div style={{ display:'flex', gap:8, marginBottom:'1rem', alignItems:'center' }}>
            <label style={{ margin:0 }}>Period:</label>
            {['1mo','3mo','6mo','1y'].map(p=>(
              <button key={p} className={`btn ${corrPeriod===p?'btn-primary':'btn-secondary'}`}
                style={{ padding:'4px 12px', fontSize:'0.78rem' }}
                onClick={()=>setCorrPeriod(p)}>{p}</button>
            ))}
          </div>
          {corrChart.length > 0 ? (
            <div className="card">
              <PlotlyChart data={corrChart}
                layout={{ title:`Stock Correlation Matrix (${corrPeriod})`, height:550 }}/>
              <div style={{ fontSize:'0.75rem', color:'var(--text-secondary)', marginTop:8 }}>
                💡 Values close to +1 = highly correlated (move together). Values close to -1 = inversely correlated (good for diversification).
              </div>
            </div>
          ) : (
            <div className="card" style={{ textAlign:'center', color:'var(--text-secondary)', padding:'2rem' }}>
              Insufficient data for correlation matrix.
            </div>
          )}
        </div>
      )}

      {tab === 'volume' && !loading && volume.length > 0 && (
        <div>
          <div className="card" style={{ marginBottom:'1rem' }}>
            <PlotlyChart data={volBar}
              layout={{ title:'Volume Ratio vs Average (>1.5x = Unusual)', height:380,
                yaxis:{title:'Volume Ratio (x)'},
                shapes:[{type:'line',x0:-0.5,x1:volume.length-0.5,y0:1.5,y1:1.5,line:{color:'#ff5252',dash:'dash',width:2}}]}}/>
          </div>
          <div className="card" style={{ overflowX:'auto' }}>
            <table>
              <thead>
                <tr>{['Symbol','Current Vol','Avg Vol','Ratio','Price Change','Alert'].map(h=><th key={h}>{h}</th>)}</tr>
              </thead>
              <tbody>
                {volume.map(v=>(
                  <tr key={v.symbol}>
                    <td style={{fontWeight:600}}>{v.symbol}</td>
                    <td>{(v.current_vol/1e6).toFixed(2)}M</td>
                    <td>{(v.avg_vol/1e6).toFixed(2)}M</td>
                    <td style={{color:v.vol_ratio>1.5?'var(--accent-red)':'var(--accent-green)',fontWeight:700}}>{v.vol_ratio}x</td>
                    <td style={{color:v.price_change>=0?'var(--accent-green)':'var(--accent-red)'}}>
                      {v.price_change>0?'+':''}{v.price_change}%
                    </td>
                    <td><span className={`badge badge-${v.alert==='High'?'red':'green'}`}>{v.alert}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab === 'breadth' && !loading && breadth && (
        <div>
          <div className="grid-2" style={{ marginBottom:'1rem' }}>
            <div className="card">
              <PlotlyChart data={breadthGauge} layout={{ height:350 }}/>
            </div>
            <div className="card">
              <div style={{ fontWeight:600, color:'var(--accent)', marginBottom:'1rem' }}>Market Breadth Details</div>
              {[
                {label:'Total Stocks',  val:breadth.total,      color:'var(--accent)'},
                {label:'Advancing',     val:breadth.advancing,  color:'var(--accent-green)'},
                {label:'Declining',     val:breadth.declining,  color:'var(--accent-red)'},
                {label:'Unchanged',     val:breadth.unchanged,  color:'var(--accent-orange)'},
                {label:'A/D Ratio',     val:breadth.ad_ratio,   color:'var(--accent)'},
                {label:'Breadth Strength',val:`${breadth.strength}%`,color:'var(--accent)'},
                {label:'Sentiment',     val:breadth.sentiment,  color:breadth.sentiment==='Bullish'?'var(--accent-green)':breadth.sentiment==='Bearish'?'var(--accent-red)':'var(--accent-orange)'},
              ].map(r=>(
                <div key={r.label} style={{display:'flex',justifyContent:'space-between',
                  padding:'9px 0',borderBottom:'1px solid var(--border)'}}>
                  <span style={{color:'var(--text-secondary)',fontSize:'0.85rem'}}>{r.label}</span>
                  <span style={{color:r.color,fontWeight:700}}>{r.val}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
