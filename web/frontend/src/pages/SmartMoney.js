import React, { useEffect, useState } from 'react';
import { smartMoney } from '../api';
import PlotlyChart from '../components/PlotlyChart';

export default function SmartMoney() {
  const [fiiDii,   setFiiDii]   = useState(null);
  const [bulk,     setBulk]     = useState([]);
  const [block,    setBlock]    = useState([]);
  const [sector,   setSector]   = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [tab,      setTab]      = useState('fiidii');

  const load = () => {
    setLoading(true);
    Promise.all([
      smartMoney.fiiDii(),
      smartMoney.bulkDeals(),
      smartMoney.blockDeals(),
      smartMoney.sectorFlow(),
    ]).then(([f, b, bl, s]) => {
      setFiiDii(f.data); setBulk(b.data); setBlock(bl.data); setSector(s.data);
    }).catch(console.error).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const sigColor = fiiDii?.signal === 'STRONG BUY' || fiiDii?.signal === 'BUY'
    ? 'var(--accent-green)' : fiiDii?.signal?.includes('SELL')
    ? 'var(--accent-red)' : 'var(--accent-orange)';

  const gaugeData = fiiDii?.fii_net != null ? [{
    type: 'indicator', mode: 'gauge+number+delta',
    value: fiiDii.fii_net,
    delta: { reference: 0, increasing: { color: '#00ff88' }, decreasing: { color: '#ff5252' } },
    number: { suffix: ' Cr', font: { color: fiiDii.fii_net >= 0 ? '#00ff88' : '#ff5252' } },
    title: { text: 'FII Net Flow Today (₹ Cr)', font: { color: '#00d4ff' } },
    gauge: {
      axis: { range: [-5000, 5000] },
      bar: { color: fiiDii.fii_net >= 0 ? '#00ff88' : '#ff5252' },
      steps: [
        { range: [-5000, -1000], color: 'rgba(255,82,82,0.2)' },
        { range: [-1000, 1000],  color: 'rgba(255,193,7,0.1)' },
        { range: [1000, 5000],   color: 'rgba(0,255,136,0.2)' },
      ],
    },
  }] : [];

  const sectorBar = sector.length ? [{
    type: 'bar',
    x: sector.map(s => s.sector),
    y: sector.map(s => s.avg_change),
    marker: { color: sector.map(s => s.avg_change >= 0 ? '#00ff88' : '#ff5252') },
    text: sector.map(s => `${s.avg_change > 0 ? '+' : ''}${s.avg_change}%`),
    textposition: 'outside',
  }] : [];

  return (
    <div>
      <div className="section-title">🏦 Smart Money Tracker</div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
          Live FII/DII from NSE API · Bulk & Block deals · Sector flow
        </div>
        <button className="btn btn-secondary" style={{ fontSize: '0.78rem' }} onClick={load}>🔄 Refresh</button>
      </div>

      {loading && <div className="loading"><div className="spinner"/><span>Fetching live institutional data...</span></div>}

      {!loading && fiiDii && (
        <>
          {/* Signal banner */}
          <div style={{ background: `${sigColor}15`, border: `1px solid ${sigColor}`,
            borderRadius: 12, padding: '1rem 1.5rem', marginBottom: '1.25rem',
            display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Market Signal · {fiiDii.date}</div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: sigColor }}>{fiiDii.signal}</div>
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textAlign: 'right' }}>
              Source: {fiiDii.source}
            </div>
          </div>

          {/* KPI row */}
          <div className="grid-4" style={{ marginBottom: '1.25rem' }}>
            {[
              { label: 'FII Net', val: fiiDii.fii_net, sub: `Buy: ₹${fiiDii.fii_buy?.toLocaleString('en-IN')} Cr` },
              { label: 'DII Net', val: fiiDii.dii_net, sub: `Buy: ₹${fiiDii.dii_buy?.toLocaleString('en-IN')} Cr` },
              { label: 'FII Buy', val: fiiDii.fii_buy, sub: 'Gross purchase' },
              { label: 'FII Sell',val: fiiDii.fii_sell,sub: 'Gross sale' },
            ].map(k => {
              const c = k.val >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
              return (
                <div key={k.label} className="kpi-card" style={{ borderLeftColor: c }}>
                  <div className="kpi-label">{k.label}</div>
                  <div className="kpi-value" style={{ color: c, fontSize: '1.3rem' }}>
                    ₹{k.val?.toLocaleString('en-IN')} Cr
                  </div>
                  <div className="kpi-sub">{k.sub}</div>
                </div>
              );
            })}
          </div>
        </>
      )}

      <div className="tab-bar">
        {[['fiidii','📊 FII/DII'],['bulk','💼 Bulk Deals'],['block','🔒 Block Deals'],['sector','🏭 Sector Flow']].map(([id,label])=>(
          <button key={id} className={`tab ${tab===id?'active':''}`} onClick={()=>setTab(id)}>{label}</button>
        ))}
      </div>

      {tab === 'fiidii' && !loading && gaugeData.length > 0 && (
        <div className="grid-2">
          <div className="card">
            <PlotlyChart data={gaugeData} layout={{ height: 320 }}/>
          </div>
          <div className="card">
            <div style={{ fontWeight: 600, color: 'var(--accent)', marginBottom: '0.75rem' }}>FII/DII Summary</div>
            {fiiDii && [
              { label: 'FII Net Flow', val: `₹${fiiDii.fii_net?.toLocaleString('en-IN')} Cr`, color: fiiDii.fii_net >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' },
              { label: 'DII Net Flow', val: `₹${fiiDii.dii_net?.toLocaleString('en-IN')} Cr`, color: fiiDii.dii_net >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' },
              { label: 'Date', val: fiiDii.date, color: 'var(--text-primary)' },
              { label: 'Data Source', val: fiiDii.source, color: 'var(--accent)' },
            ].map(r => (
              <div key={r.label} style={{ display: 'flex', justifyContent: 'space-between',
                padding: '10px 0', borderBottom: '1px solid var(--border)' }}>
                <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{r.label}</span>
                <span style={{ color: r.color, fontWeight: 600 }}>{r.val}</span>
              </div>
            ))}
            <div style={{ marginTop: 12, fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
              ℹ️ Today's data is real NSE API. Historical rows are Nifty-proxy estimates.
            </div>
          </div>
        </div>
      )}

      {tab === 'bulk' && !loading && (
        <div>
          {bulk.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem' }}>
              No bulk deals today or NSE data not yet available.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {bulk.map((d, i) => {
                const c = d.type?.toUpperCase().includes('BUY') ? 'var(--accent-green)' : 'var(--accent-red)';
                return (
                  <div key={i} className="card" style={{ borderLeft: `3px solid ${c}` }}>
                    <div style={{ fontWeight: 600 }}>{d.company} ({d.symbol})</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: 4 }}>
                      Client: {d.client} · Type: <span style={{ color: c }}>{d.type}</span> ·
                      Qty: {d.qty?.toLocaleString('en-IN')} · Price: ₹{d.price} · {d.date}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {tab === 'block' && !loading && (
        <div>
          {block.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem' }}>
              No block deals today.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {block.map((d, i) => (
                <div key={i} className="card" style={{ borderLeft: '3px solid #764ba2' }}>
                  <div style={{ fontWeight: 600 }}>{d.company} ({d.symbol})</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: 4 }}>
                    Client: {d.client} · Qty: {d.qty?.toLocaleString('en-IN')} · Price: ₹{d.price} · {d.date}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {tab === 'sector' && !loading && sectorBar.length > 0 && (
        <div className="card">
          <PlotlyChart data={sectorBar}
            layout={{ title: 'Sector-wise Money Flow Today (%)', height: 400,
              yaxis: { title: '% Change' }, shapes: [{ type:'line', x0:-0.5, x1:sector.length-0.5, y0:0, y1:0, line:{color:'#555',dash:'dash'} }] }}/>
        </div>
      )}
    </div>
  );
}
