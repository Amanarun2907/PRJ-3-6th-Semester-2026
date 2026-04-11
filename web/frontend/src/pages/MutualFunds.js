import React, { useEffect, useState } from 'react';
import { mf } from '../api';
import PlotlyChart from '../components/PlotlyChart';

export default function MutualFunds() {
  const [categories, setCategories] = useState([]);
  const [category,   setCategory]   = useState('Large Cap');
  const [funds,      setFunds]      = useState([]);
  const [selected,   setSelected]   = useState(null);
  const [navHist,    setNavHist]    = useState(null);
  const [loading,    setLoading]    = useState(false);

  useEffect(() => {
    mf.categories().then(r => { setCategories(r.data); });
  }, []);

  useEffect(() => {
    setLoading(true); setFunds([]); setSelected(null); setNavHist(null);
    mf.funds(category, 20).then(r => setFunds(r.data.funds || []))
      .catch(console.error).finally(() => setLoading(false));
  }, [category]);

  const loadNav = (fund) => {
    setSelected(fund);
    mf.navHistory(fund.scheme_code, 365).then(r => setNavHist(r.data));
  };

  const navChart = navHist ? [{
    type: 'scatter', x: navHist.dates, y: navHist.navs,
    line: { color: '#00d4ff', width: 2 }, fill: 'tozeroy',
    fillcolor: 'rgba(0,212,255,0.08)', name: 'NAV',
  }] : [];

  return (
    <div>
      <div className="section-title">💰 Mutual Fund Center</div>

      <div style={{ marginBottom: '1.25rem' }}>
        <label>Category</label>
        <select value={category} onChange={e => setCategory(e.target.value)} style={{ maxWidth: 280 }}>
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      {loading && <div className="loading"><div className="spinner"/><span>Fetching live AMFI data...</span></div>}

      {!loading && funds.length > 0 && (
        <div className="grid-2">
          <div>
            <div style={{ fontWeight: 600, color: 'var(--accent)', marginBottom: '0.75rem' }}>
              {funds.length} funds — Direct Growth · Live NAV from AMFI
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8, maxHeight: 600, overflowY: 'auto' }}>
              {funds.map(f => (
                <div key={f.scheme_code} className="card"
                  style={{ cursor: 'pointer', borderColor: selected?.scheme_code === f.scheme_code ? 'var(--accent)' : 'var(--border)' }}
                  onClick={() => loadNav(f)}>
                  <div style={{ fontWeight: 600, fontSize: '0.85rem', marginBottom: 6 }}>{f.name}</div>
                  <div style={{ display: 'flex', gap: 16, fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                    <span>NAV: <strong style={{ color: 'var(--accent)' }}>₹{f.nav?.toFixed(2)}</strong></span>
                    {f.return_1y != null && <span>1Y: <strong style={{ color: f.return_1y >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>{f.return_1y?.toFixed(2)}%</strong></span>}
                    {f.return_3y != null && <span>3Y: <strong style={{ color: f.return_3y >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>{f.return_3y?.toFixed(2)}%</strong></span>}
                  </div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', marginTop: 4 }}>
                    Code: {f.scheme_code} · {f.nav_date}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            {selected && navHist ? (
              <div className="card">
                <div style={{ fontWeight: 600, color: 'var(--accent)', marginBottom: '0.75rem', fontSize: '0.85rem' }}>
                  📈 NAV History — {selected.name.slice(0,50)}
                </div>
                <PlotlyChart data={navChart}
                  layout={{ title: '1-Year NAV History', height: 380,
                    yaxis: { title: 'NAV (₹)' }, xaxis: { title: 'Date' } }}/>
              </div>
            ) : (
              <div className="card" style={{ display: 'flex', alignItems: 'center',
                justifyContent: 'center', height: 300, color: 'var(--text-secondary)' }}>
                👆 Click a fund to see NAV history
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
