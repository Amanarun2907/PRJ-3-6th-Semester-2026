import React, { useEffect, useState } from 'react';
import { portfolio } from '../api';
import PlotlyChart from '../components/PlotlyChart';
import toast from 'react-hot-toast';

const STOCKS = [
  'HDFCBANK','ICICIBANK','KOTAKBANK','SBIN','AXISBANK','INDUSINDBK','BAJFINANCE','BAJAJFINSV',
  'TCS','INFY','WIPRO','HCLTECH','TECHM','RELIANCE','ONGC','NTPC','COALINDIA',
  'HINDUNILVR','ITC','NESTLEIND','BRITANNIA','DABUR',
  'MARUTI','TATAMOTORS','BAJAJ-AUTO','HEROMOTOCO','M&M',
  'SUNPHARMA','DRREDDY','CIPLA','DIVISLAB','APOLLOHOSP',
  'TATASTEEL','HINDALCO','JSWSTEEL','LT','ULTRACEMCO',
  'BHARTIARTL','TITAN','ASIANPAINT','ADANIPORTS',
];
const SECTORS = ['Banking','IT','Pharma','Auto','Energy','FMCG','Metals','Realty','Telecom','Others'];

export default function PortfolioManager() {
  const [holdings, setHoldings] = useState([]);
  const [metrics,  setMetrics]  = useState(null);
  const [loading,  setLoading]  = useState(true);
  const [tab,      setTab]      = useState('holdings');
  const [adding,   setAdding]   = useState(false);
  const [form, setForm] = useState({
    symbol:'HDFCBANK', quantity:10, buy_price:1600,
    sector:'Banking', buy_date: new Date().toISOString().split('T')[0],
  });

  const load = () => {
    setLoading(true);
    Promise.all([portfolio.holdings(), portfolio.metrics()])
      .then(([h, m]) => { setHoldings(h.data); setMetrics(m.data); })
      .catch(console.error).finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const addHolding = async () => {
    setAdding(true);
    try {
      await portfolio.add({ ...form, company_name: form.symbol });
      toast.success(`✅ Added ${form.symbol} to portfolio!`);
      load(); setTab('holdings');
    } catch (e) { toast.error('Failed to add holding'); }
    finally { setAdding(false); }
  };

  const deleteHolding = async (id, name) => {
    await portfolio.delete(id);
    toast.success(`Removed ${name}`);
    load();
  };

  const totalInvested = holdings.reduce((a,h) => a + h.invested, 0);
  const totalCurrent  = holdings.reduce((a,h) => a + h.current_value, 0);
  const totalPnl      = totalCurrent - totalInvested;
  const totalPnlPct   = totalInvested > 0 ? (totalPnl/totalInvested*100) : 0;

  const allocationPie = holdings.length ? [{
    type:'pie',
    labels: holdings.map(h => h.symbol),
    values: holdings.map(h => h.current_value),
    marker:{ line:{color:'#060910',width:2} },
    hole:0.45, textinfo:'label+percent',
    textfont:{ color:'#f0f6fc', size:10 },
    hovertemplate:'<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>',
  }] : [];

  const pnlBar = holdings.length ? [{
    type:'bar', orientation:'h',
    x: holdings.map(h => h.pnl),
    y: holdings.map(h => h.symbol),
    marker:{ color: holdings.map(h => h.pnl >= 0 ? 'rgba(0,255,136,0.7)' : 'rgba(255,71,87,0.7)'),
      line:{ color: holdings.map(h => h.pnl >= 0 ? '#00ff88' : '#ff4757'), width:1 } },
    text: holdings.map(h => `₹${h.pnl?.toLocaleString('en-IN')}`),
    textposition:'outside',
    hovertemplate:'<b>%{y}</b><br>P&L: ₹%{x:,.0f}<extra></extra>',
  }] : [];

  const pnlPctBar = holdings.length ? [{
    type:'bar',
    x: holdings.map(h => h.symbol),
    y: holdings.map(h => h.pnl_pct),
    marker:{ color: holdings.map(h => h.pnl_pct >= 0 ? 'rgba(0,255,136,0.7)' : 'rgba(255,71,87,0.7)') },
    text: holdings.map(h => `${h.pnl_pct > 0?'+':''}${h.pnl_pct?.toFixed(1)}%`),
    textposition:'outside',
    hovertemplate:'<b>%{x}</b><br>Return: %{y:.2f}%<extra></extra>',
  }] : [];

  const pnlColor = totalPnl >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';

  return (
    <div>
      <div className="page-header">
        <div className="section-title">🛡️ Portfolio & Risk Manager</div>
        <div className="section-subtitle">
          <span className="pulse-dot"/>
          Live prices from Yahoo Finance · Real P&L · Risk metrics
          <button className="btn btn-secondary" style={{ marginLeft:'auto', padding:'5px 12px', fontSize:'0.75rem' }}
            onClick={load}>🔄 Refresh</button>
        </div>
      </div>

      {/* Summary KPIs */}
      {!loading && holdings.length > 0 && (
        <div className="grid-4" style={{ marginBottom:'1.25rem' }}>
          {[
            { label:'Total Invested',  val:`₹${totalInvested.toLocaleString('en-IN')}`,  color:'var(--accent)' },
            { label:'Current Value',   val:`₹${totalCurrent.toLocaleString('en-IN')}`,   color:'var(--accent)' },
            { label:'Total P&L',       val:`₹${totalPnl.toLocaleString('en-IN')}`,       color:pnlColor },
            { label:'Overall Return',  val:`${totalPnlPct > 0?'+':''}${totalPnlPct.toFixed(2)}%`, color:pnlColor },
          ].map(k => (
            <div key={k.label} className="kpi-card" style={{ borderLeftColor:k.color }}>
              <div className="kpi-label">{k.label}</div>
              <div className="kpi-value" style={{ color:k.color, fontSize:'1.3rem' }}>{k.val}</div>
            </div>
          ))}
        </div>
      )}

      <div className="tab-bar">
        {[
          ['holdings','💼 My Holdings'],
          ['add','➕ Add Stock'],
          ['analysis','📊 Analysis'],
        ].map(([id,label]) => (
          <button key={id} className={`tab ${tab===id?'active':''}`} onClick={() => setTab(id)}>{label}</button>
        ))}
      </div>

      {tab === 'holdings' && (
        <>
          {loading && <div className="loading"><div className="spinner"/><div className="loading-text">Fetching live prices...</div></div>}
          {!loading && holdings.length === 0 && (
            <div className="card" style={{ textAlign:'center', padding:'3rem' }}>
              <div style={{ fontSize:'2rem', marginBottom:'1rem' }}>📭</div>
              <div style={{ fontWeight:600, color:'var(--text-secondary)', marginBottom:'0.5rem' }}>
                Portfolio is empty
              </div>
              <div style={{ fontSize:'0.85rem', color:'var(--text-muted)', marginBottom:'1.5rem' }}>
                Add your first stock to start tracking real-time P&L
              </div>
              <button className="btn btn-primary" onClick={() => setTab('add')}>➕ Add Your First Stock</button>
            </div>
          )}
          {!loading && holdings.length > 0 && (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    {['Stock','Sector','Qty','Buy ₹','Current ₹','Today %','P&L ₹','Return %','Action'].map(h=>(
                      <th key={h}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {holdings.map(h => {
                    const pc = h.pnl_pct >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
                    const tc = h.today_change_pct >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
                    return (
                      <tr key={h.id}>
                        <td><span style={{ fontWeight:700, color:'var(--accent)' }}>{h.symbol}</span></td>
                        <td><span className="badge badge-blue" style={{ fontSize:'0.65rem' }}>{h.sector}</span></td>
                        <td>{h.quantity}</td>
                        <td>₹{h.buy_price?.toLocaleString('en-IN')}</td>
                        <td style={{ fontWeight:600 }}>₹{h.current_price?.toLocaleString('en-IN')}</td>
                        <td style={{ color:tc, fontWeight:600 }}>
                          {h.today_change_pct > 0?'+':''}{h.today_change_pct?.toFixed(2)}%
                        </td>
                        <td style={{ color:pc, fontWeight:600 }}>₹{h.pnl?.toLocaleString('en-IN')}</td>
                        <td>
                          <span style={{ color:pc, fontWeight:700 }}>
                            {h.pnl_pct > 0?'+':''}{h.pnl_pct?.toFixed(2)}%
                          </span>
                        </td>
                        <td>
                          <button className="btn btn-danger" style={{ padding:'4px 10px', fontSize:'0.72rem' }}
                            onClick={() => deleteHolding(h.id, h.symbol)}>🗑️</button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      {tab === 'add' && (
        <div className="card" style={{ maxWidth:560 }}>
          <div style={{ fontWeight:700, color:'var(--accent)', marginBottom:'1.25rem', fontSize:'1rem' }}>
            ➕ Add Stock to Portfolio
          </div>
          <div style={{ display:'flex', flexDirection:'column', gap:14 }}>
            <div>
              <label>Stock Symbol</label>
              <select value={form.symbol} onChange={e => setForm({...form, symbol:e.target.value})}>
                {STOCKS.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div className="grid-2">
              <div>
                <label>Quantity (shares)</label>
                <input type="number" value={form.quantity} min={1}
                  onChange={e => setForm({...form, quantity:Number(e.target.value)})}/>
              </div>
              <div>
                <label>Buy Price (₹)</label>
                <input type="number" value={form.buy_price} step={0.01}
                  onChange={e => setForm({...form, buy_price:Number(e.target.value)})}/>
              </div>
            </div>
            <div className="grid-2">
              <div>
                <label>Sector</label>
                <select value={form.sector} onChange={e => setForm({...form, sector:e.target.value})}>
                  {SECTORS.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label>Buy Date</label>
                <input type="date" value={form.buy_date}
                  onChange={e => setForm({...form, buy_date:e.target.value})}/>
              </div>
            </div>
            <div className="card-glow" style={{ textAlign:'center', padding:'0.75rem' }}>
              <div style={{ fontSize:'0.72rem', color:'var(--text-secondary)', marginBottom:3 }}>TOTAL INVESTMENT</div>
              <div style={{ fontSize:'1.4rem', fontWeight:800, color:'var(--accent)' }}>
                ₹{(form.quantity * form.buy_price).toLocaleString('en-IN')}
              </div>
            </div>
            <button className="btn btn-primary" onClick={addHolding} disabled={adding}
              style={{ width:'100%', padding:'12px', fontSize:'0.95rem' }}>
              {adding ? <><div className="spinner-sm"/> Adding...</> : '➕ Add to Portfolio'}
            </button>
          </div>
        </div>
      )}

      {tab === 'analysis' && !loading && holdings.length > 0 && (
        <div style={{ display:'flex', flexDirection:'column', gap:'1rem' }}>
          <div className="grid-2">
            <div className="card">
              <PlotlyChart data={allocationPie}
                layout={{ title:'Portfolio Allocation by Stock', height:400, showlegend:true,
                  legend:{orientation:'v'} }}/>
            </div>
            <div className="card">
              <PlotlyChart data={pnlBar}
                layout={{ title:'P&L per Stock (₹)', height:400,
                  xaxis:{title:'₹ P&L', tickformat:',.0f'},
                  shapes:[{type:'line',y0:-0.5,y1:holdings.length-0.5,x0:0,x1:0,
                    line:{color:'#30363d',dash:'dash'}}] }}/>
            </div>
          </div>
          <div className="card">
            <PlotlyChart data={pnlPctBar}
              layout={{ title:'Return % per Stock', height:320,
                yaxis:{title:'Return %', ticksuffix:'%'},
                shapes:[{type:'line',x0:-0.5,x1:holdings.length-0.5,y0:0,y1:0,
                  line:{color:'#30363d',dash:'dash'}}] }}/>
          </div>
        </div>
      )}
      {tab === 'analysis' && !loading && holdings.length === 0 && (
        <div className="card" style={{ textAlign:'center', color:'var(--text-secondary)', padding:'3rem' }}>
          Add stocks to see analysis charts.
        </div>
      )}
    </div>
  );
}
