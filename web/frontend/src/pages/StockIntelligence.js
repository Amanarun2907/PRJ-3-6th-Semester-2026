import React, { useEffect, useState } from 'react';
import { stocks } from '../api';
import PlotlyChart from '../components/PlotlyChart';

const PERIODS = [
  { val:'1mo', label:'1M' }, { val:'3mo', label:'3M' },
  { val:'6mo', label:'6M' }, { val:'1y',  label:'1Y' },
  { val:'2y',  label:'2Y' },
];

export default function StockIntelligence() {
  const [stockList, setStockList] = useState([]);
  const [selected,  setSelected]  = useState('HDFCBANK');
  const [period,    setPeriod]    = useState('6mo');
  const [ohlcv,     setOhlcv]     = useState(null);
  const [tech,      setTech]      = useState(null);
  const [fund,      setFund]      = useState(null);
  const [loading,   setLoading]   = useState(false);
  const [tab,       setTab]       = useState('chart');

  useEffect(() => { stocks.list().then(r => setStockList(r.data)); }, []);

  useEffect(() => {
    if (!selected) return;
    setLoading(true); setOhlcv(null); setTech(null); setFund(null);
    Promise.all([stocks.ohlcv(selected, period), stocks.technicals(selected), stocks.fundamentals(selected)])
      .then(([o, t, f]) => { setOhlcv(o.data); setTech(t.data); setFund(f.data); })
      .catch(console.error).finally(() => setLoading(false));
  }, [selected, period]);

  const sigColor = tech?.signal === 'BUY' ? 'var(--accent-green)'
                 : tech?.signal === 'SELL' ? 'var(--accent-red)' : 'var(--accent-orange)';
  const sigBg    = tech?.signal === 'BUY' ? 'rgba(0,255,136,0.1)'
                 : tech?.signal === 'SELL' ? 'rgba(255,71,87,0.1)' : 'rgba(255,165,2,0.1)';

  const candlestick = ohlcv ? [{
    type: 'candlestick',
    x: ohlcv.dates, open: ohlcv.open, high: ohlcv.high, low: ohlcv.low, close: ohlcv.close,
    increasing: { line: { color: '#00ff88' }, fillcolor: 'rgba(0,255,136,0.7)' },
    decreasing: { line: { color: '#ff4757' }, fillcolor: 'rgba(255,71,87,0.7)' },
    name: selected,
    hovertemplate: '<b>%{x}</b><br>O: %{open}<br>H: %{high}<br>L: %{low}<br>C: %{close}<extra></extra>',
  }] : [];

  // Add MA lines to candlestick
  const maLines = tech ? [
    { type:'scatter', x:tech.dates, y:tech.ma20,  name:'MA20',  line:{color:'#ffa502',width:1.5,dash:'dot'}, hoverinfo:'skip' },
    { type:'scatter', x:tech.dates, y:tech.ma50,  name:'MA50',  line:{color:'#a855f7',width:1.5,dash:'dot'}, hoverinfo:'skip' },
    { type:'scatter', x:tech.dates, y:tech.ma200, name:'MA200', line:{color:'#00d4ff',width:1.5,dash:'dot'}, hoverinfo:'skip' },
  ] : [];

  const volumeBar = ohlcv ? [{
    type: 'bar', x: ohlcv.dates,
    y: ohlcv.volume,
    marker: { color: ohlcv.close?.map((c, i) => i > 0 && c >= ohlcv.close[i-1] ? 'rgba(0,255,136,0.5)' : 'rgba(255,71,87,0.5)') },
    name: 'Volume',
    hovertemplate: '<b>%{x}</b><br>Volume: %{y:,.0f}<extra></extra>',
  }] : [];

  const rsiChart = tech ? [{
    type: 'scatter', x: tech.dates, y: tech.rsi,
    line: { color: '#ffa502', width: 2 }, name: 'RSI',
    fill: 'tozeroy', fillcolor: 'rgba(255,165,2,0.05)',
    hovertemplate: '<b>RSI</b>: %{y:.1f}<extra></extra>',
  }] : [];

  const macdChart = tech ? [
    { type:'scatter', x:tech.dates, y:tech.macd,
      line:{color:'#00d4ff',width:2}, name:'MACD',
      hovertemplate:'MACD: %{y:.3f}<extra></extra>' },
    { type:'scatter', x:tech.dates, y:tech.macd_signal,
      line:{color:'#ff4757',width:1.5,dash:'dot'}, name:'Signal',
      hovertemplate:'Signal: %{y:.3f}<extra></extra>' },
    { type:'bar', x:tech.dates,
      y:tech.macd?.map((v,i) => v - (tech.macd_signal?.[i] || 0)),
      marker:{color:tech.macd?.map((v,i) => v >= (tech.macd_signal?.[i]||0) ? 'rgba(0,255,136,0.4)' : 'rgba(255,71,87,0.4)')},
      name:'Histogram' },
  ] : [];

  const bbChart = tech ? [
    { type:'scatter', x:tech.dates, y:tech.bb_upper,
      line:{color:'rgba(0,212,255,0.5)',width:1,dash:'dot'}, name:'Upper BB', hoverinfo:'skip' },
    { type:'scatter', x:tech.dates, y:tech.bb_lower,
      line:{color:'rgba(0,212,255,0.5)',width:1,dash:'dot'}, name:'Lower BB',
      fill:'tonexty', fillcolor:'rgba(0,212,255,0.04)', hoverinfo:'skip' },
    { type:'scatter', x:tech.dates, y:tech.close,
      line:{color:'#f0f6fc',width:2}, name:'Price',
      hovertemplate:'₹%{y:.2f}<extra></extra>' },
    { type:'scatter', x:tech.dates, y:tech.bb_mid,
      line:{color:'rgba(255,165,2,0.6)',width:1,dash:'dot'}, name:'Mid BB', hoverinfo:'skip' },
  ] : [];

  const selectedStock = stockList.find(s => s.symbol === selected);

  return (
    <div>
      <div className="page-header">
        <div className="section-title">📊 Stock Intelligence</div>
        <div className="section-subtitle">
          <span className="pulse-dot"/>
          Live OHLCV · Technical Indicators · Fundamentals · 50+ NSE stocks
        </div>
      </div>

      {/* Controls bar */}
      <div className="card" style={{ marginBottom: '1.25rem', padding: '1rem 1.25rem' }}>
        <div style={{ display: 'flex', gap: 16, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: 220 }}>
            <label>Select Stock</label>
            <select value={selected} onChange={e => setSelected(e.target.value)}>
              {stockList.map(s => <option key={s.symbol} value={s.symbol}>{s.name} ({s.symbol})</option>)}
            </select>
          </div>
          <div>
            <label>Time Period</label>
            <div style={{ display: 'flex', gap: 4 }}>
              {PERIODS.map(p => (
                <button key={p.val} className={`btn ${period===p.val?'btn-primary':'btn-secondary'}`}
                  style={{ padding: '7px 14px', fontSize: '0.8rem' }}
                  onClick={() => setPeriod(p.val)}>{p.label}</button>
              ))}
            </div>
          </div>
          {tech?.signal && (
            <div style={{ background: sigBg, border: `1px solid ${sigColor}`,
              borderRadius: 10, padding: '8px 20px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)', marginBottom: 2 }}>AI SIGNAL</div>
              <div style={{ fontWeight: 800, color: sigColor, fontSize: '1.1rem' }}>{tech.signal}</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>RSI: {tech.rsi_latest}</div>
            </div>
          )}
        </div>
      </div>

      {loading && (
        <div className="loading">
          <div className="spinner"/>
          <div className="loading-text">Fetching live data for {selectedStock?.name || selected}...</div>
        </div>
      )}

      {!loading && (
        <>
          <div className="tab-bar">
            {[
              { id:'chart',        label:'📈 Price Chart' },
              { id:'technicals',   label:'🔧 Technical Analysis' },
              { id:'fundamentals', label:'📋 Fundamentals' },
            ].map(t => (
              <button key={t.id} className={`tab ${tab===t.id?'active':''}`} onClick={() => setTab(t.id)}>
                {t.label}
              </button>
            ))}
          </div>

          {tab === 'chart' && ohlcv && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                  <div style={{ fontWeight: 700, color: 'var(--accent)' }}>
                    {selectedStock?.name} — Candlestick Chart
                  </div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                    {ohlcv.dates?.length} trading days
                  </div>
                </div>
                <PlotlyChart data={[...candlestick, ...maLines]}
                  layout={{ height: 460,
                    xaxis: { rangeslider: { visible: false }, type: 'date' },
                    yaxis: { title: 'Price (₹)', tickprefix: '₹' },
                    legend: { orientation: 'h', y: 1.05 },
                  }}/>
              </div>
              <div className="card">
                <div style={{ fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 6, fontSize: '0.82rem' }}>
                  📊 Volume (green = up day, red = down day)
                </div>
                <PlotlyChart data={volumeBar}
                  layout={{ height: 180, showlegend: false,
                    yaxis: { title: 'Volume', tickformat: '.2s' } }}/>
              </div>
            </div>
          )}

          {tab === 'technicals' && tech && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {/* Signal summary */}
              <div className="card-glow">
                <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', alignItems: 'center' }}>
                  <div style={{ background: sigBg, border: `1px solid ${sigColor}`,
                    borderRadius: 10, padding: '12px 24px', textAlign: 'center' }}>
                    <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)' }}>SIGNAL</div>
                    <div style={{ fontWeight: 900, color: sigColor, fontSize: '1.5rem' }}>{tech.signal}</div>
                  </div>
                  {[
                    { label: 'RSI (14)', val: tech.rsi_latest?.toFixed(1),
                      color: tech.rsi_latest > 70 ? 'var(--accent-red)' : tech.rsi_latest < 30 ? 'var(--accent-green)' : 'var(--accent)' },
                    { label: 'MA20 vs Price', val: tech.close?.at(-1) > tech.ma20?.at(-1) ? 'Above ↑' : 'Below ↓',
                      color: tech.close?.at(-1) > tech.ma20?.at(-1) ? 'var(--accent-green)' : 'var(--accent-red)' },
                    { label: 'MA50 vs Price', val: tech.close?.at(-1) > tech.ma50?.at(-1) ? 'Above ↑' : 'Below ↓',
                      color: tech.close?.at(-1) > tech.ma50?.at(-1) ? 'var(--accent-green)' : 'var(--accent-red)' },
                    { label: 'MACD', val: tech.macd?.at(-1) > tech.macd_signal?.at(-1) ? 'Bullish ↑' : 'Bearish ↓',
                      color: tech.macd?.at(-1) > tech.macd_signal?.at(-1) ? 'var(--accent-green)' : 'var(--accent-red)' },
                  ].map(s => (
                    <div key={s.label} style={{ textAlign: 'center', padding: '8px 16px',
                      background: 'var(--bg-secondary)', borderRadius: 8 }}>
                      <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)', marginBottom: 3 }}>{s.label}</div>
                      <div style={{ fontWeight: 700, color: s.color }}>{s.val}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid-2">
                <div className="card">
                  <PlotlyChart data={rsiChart}
                    layout={{ title: 'RSI (14) — Overbought >70 | Oversold <30', height: 280,
                      yaxis: { range: [0, 100] },
                      shapes: [
                        { type:'line', x0:tech.dates[0], x1:tech.dates.at(-1), y0:70, y1:70,
                          line:{color:'rgba(255,71,87,0.5)',dash:'dot',width:1.5} },
                        { type:'rect', x0:tech.dates[0], x1:tech.dates.at(-1), y0:70, y1:100,
                          fillcolor:'rgba(255,71,87,0.04)', line:{width:0} },
                        { type:'line', x0:tech.dates[0], x1:tech.dates.at(-1), y0:30, y1:30,
                          line:{color:'rgba(0,255,136,0.5)',dash:'dot',width:1.5} },
                        { type:'rect', x0:tech.dates[0], x1:tech.dates.at(-1), y0:0, y1:30,
                          fillcolor:'rgba(0,255,136,0.04)', line:{width:0} },
                      ]}}/>
                </div>
                <div className="card">
                  <PlotlyChart data={macdChart}
                    layout={{ title: 'MACD (12,26,9)', height: 280, barmode: 'overlay' }}/>
                </div>
              </div>
              <div className="card">
                <PlotlyChart data={bbChart}
                  layout={{ title: 'Bollinger Bands (20,2) — Price with Upper/Lower bands', height: 360,
                    yaxis: { tickprefix: '₹' } }}/>
              </div>
            </div>
          )}

          {tab === 'fundamentals' && fund && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="card-glow">
                <div style={{ fontWeight: 800, fontSize: '1.2rem', color: 'var(--accent)', marginBottom: 4 }}>
                  {fund.name}
                </div>
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                  <span className="badge badge-blue">{fund.sector}</span>
                  <span className="badge badge-green">NSE Listed</span>
                </div>
                {fund.description && (
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem',
                    lineHeight: 1.7, marginTop: '0.75rem', borderTop: '1px solid var(--border)', paddingTop: '0.75rem' }}>
                    {fund.description}
                  </div>
                )}
              </div>
              <div className="grid-4">
                {[
                  { label: 'Market Cap',     val: fund.market_cap ? `₹${(fund.market_cap/1e12).toFixed(2)}T` : 'N/A', icon: '🏢' },
                  { label: 'P/E Ratio',      val: fund.pe_ratio?.toFixed(2) || 'N/A', icon: '📊' },
                  { label: 'P/B Ratio',      val: fund.pb_ratio?.toFixed(2) || 'N/A', icon: '📚' },
                  { label: 'Dividend Yield', val: fund.dividend_yield ? `${(fund.dividend_yield*100).toFixed(2)}%` : 'N/A', icon: '💸' },
                  { label: '52W High',       val: `₹${fund.week_52_high?.toFixed(2)}`, icon: '⬆️' },
                  { label: '52W Low',        val: `₹${fund.week_52_low?.toFixed(2)}`, icon: '⬇️' },
                  { label: 'Avg Volume',     val: fund.avg_volume ? `${(fund.avg_volume/1e6).toFixed(2)}M` : 'N/A', icon: '📈' },
                  { label: 'Sector',         val: fund.sector || 'N/A', icon: '🏭' },
                ].map(r => (
                  <div key={r.label} className="card" style={{ padding: '1rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '1.3rem', marginBottom: 6 }}>{r.icon}</div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginBottom: 4,
                      textTransform: 'uppercase', letterSpacing: '0.05em' }}>{r.label}</div>
                    <div style={{ fontWeight: 700, color: 'var(--accent)', fontSize: '1rem' }}>{r.val}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
