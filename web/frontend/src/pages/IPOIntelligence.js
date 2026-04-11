import React, { useEffect, useState } from 'react';
import { ipo } from '../api';
import PlotlyChart from '../components/PlotlyChart';

const C = {
  Open:     '#00ff88',
  Upcoming: '#00d4ff',
  Closed:   '#8b949e',
  Unknown:  '#ffa502',
};
const REC_C = { APPLY: '#00ff88', AVOID: '#ff4757', NEUTRAL: '#ffa502' };
const REC_ICON = { APPLY: '✅', AVOID: '❌', NEUTRAL: '⚠️' };

/* SVG circular score ring */
function ScoreRing({ score }) {
  const color = score >= 65 ? '#00ff88' : score >= 45 ? '#ffa502' : '#ff4757';
  const r = 24, circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  return (
    <div style={{ position: 'relative', width: 64, height: 64, flexShrink: 0 }}>
      <svg width="64" height="64" style={{ transform: 'rotate(-90deg)' }}>
        <circle cx="32" cy="32" r={r} fill="none" stroke="#21262d" strokeWidth="5" />
        <circle cx="32" cy="32" r={r} fill="none" stroke={color} strokeWidth="5"
          strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
          style={{ transition: 'stroke-dasharray 0.8s ease' }} />
      </svg>
      <div style={{ position: 'absolute', inset: 0,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ fontSize: '0.85rem', fontWeight: 900, color, lineHeight: 1 }}>{score}</div>
        <div style={{ fontSize: '0.5rem', color: '#8b949e' }}>/100</div>
      </div>
    </div>
  );
}

/* Status pill */
function StatusPill({ status }) {
  const color = C[status] || '#8b949e';
  return (
    <span style={{
      background: color + '18', color, border: `1px solid ${color}44`,
      borderRadius: 20, padding: '3px 10px', fontSize: '0.72rem', fontWeight: 700,
      display: 'inline-flex', alignItems: 'center', gap: 4,
    }}>
      <span style={{ width: 6, height: 6, borderRadius: '50%', background: color,
        animation: status === 'Open' ? 'pulse 1.5s infinite' : 'none' }} />
      {status}
    </span>
  );
}

/* Full IPO card */
function IPOCard({ item }) {
  const [expanded, setExpanded] = useState(false);
  const rc = REC_C[item.recommendation] || '#ffa502';
  const sc = C[item.status] || '#8b949e';

  return (
    <div className="card" style={{
      borderTop: `3px solid ${sc}`,
      transition: 'all 0.25s',
      cursor: 'pointer',
    }} onClick={() => setExpanded(!expanded)}>
      {/* Top row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 10 }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 700, fontSize: '0.95rem', lineHeight: 1.3, marginBottom: 6 }}>
            {item.name}
          </div>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            <StatusPill status={item.status} />
            <span style={{
              background: 'rgba(168,85,247,0.12)', color: '#a855f7',
              border: '1px solid rgba(168,85,247,0.25)',
              borderRadius: 20, padding: '3px 10px', fontSize: '0.68rem', fontWeight: 600,
            }}>{item.category}</span>
          </div>
        </div>
        <ScoreRing score={item.score || 50} />
      </div>

      {/* Key info grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px 16px',
        marginTop: 12, fontSize: '0.78rem' }}>
        {[
          { label: 'Price Band',  val: item.price_band  || 'TBA' },
          { label: 'Issue Size',  val: item.issue_size  || 'N/A' },
          { label: 'Open Date',   val: item.open_date   || 'N/A' },
          { label: 'Close Date',  val: item.close_date  || 'N/A' },
        ].map(r => (
          <div key={r.label}>
            <div style={{ color: '#8b949e', fontSize: '0.65rem', marginBottom: 1,
              textTransform: 'uppercase', letterSpacing: '0.04em' }}>{r.label}</div>
            <div style={{ fontWeight: 600 }}>{r.val}</div>
          </div>
        ))}
      </div>

      {/* Expanded details */}
      {expanded && (
        <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid var(--border)',
          display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px 16px', fontSize: '0.78rem' }}>
          {[
            { label: 'Subscription', val: item.subscription || 'N/A' },
            { label: 'GMP',          val: item.gmp          || 'N/A' },
            { label: 'Listing Date', val: item.listing_date || 'N/A' },
            { label: 'Source',       val: item.source       || 'N/A' },
          ].map(r => (
            <div key={r.label}>
              <div style={{ color: '#8b949e', fontSize: '0.65rem', marginBottom: 1,
                textTransform: 'uppercase', letterSpacing: '0.04em' }}>{r.label}</div>
              <div style={{ fontWeight: 600 }}>{r.val}</div>
            </div>
          ))}
        </div>
      )}

      {/* Recommendation */}
      <div style={{ marginTop: 12, textAlign: 'center' }}>
        <span style={{
          background: rc + '15', color: rc, border: `1px solid ${rc}33`,
          borderRadius: 8, padding: '6px 24px',
          fontWeight: 800, fontSize: '0.85rem', letterSpacing: '0.06em',
        }}>
          {REC_ICON[item.recommendation]} {item.recommendation}
        </span>
      </div>

      <div style={{ textAlign: 'center', marginTop: 6, fontSize: '0.65rem', color: '#484f58' }}>
        {expanded ? '▲ Click to collapse' : '▼ Click for more details'}
      </div>
    </div>
  );
}

export default function IPOIntelligence() {
  const [data,    setData]    = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter,  setFilter]  = useState('All');
  const [view,    setView]    = useState('cards');

  const load = () => {
    setLoading(true);
    ipo.live()
      .then(r => setData(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const ipos     = data?.ipos || [];
  const filtered = filter === 'All' ? ipos : ipos.filter(i => i.status === filter);

  /* ── Charts ── */
  const scoreBar = ipos.slice(0, 15).length ? [{
    type: 'bar',
    x: ipos.slice(0, 15).map(i => i.name?.slice(0, 18) + (i.name?.length > 18 ? '…' : '')),
    y: ipos.slice(0, 15).map(i => i.score),
    marker: {
      color: ipos.slice(0, 15).map(i =>
        i.score >= 65 ? 'rgba(0,255,136,0.75)' :
        i.score >= 45 ? 'rgba(255,165,2,0.75)' : 'rgba(255,71,87,0.75)'),
      line: { color: ipos.slice(0, 15).map(i =>
        i.score >= 65 ? '#00ff88' : i.score >= 45 ? '#ffa502' : '#ff4757'), width: 1 },
    },
    text: ipos.slice(0, 15).map(i => i.score + '/100'),
    textposition: 'outside',
    textfont: { size: 10 },
    hovertemplate: '<b>%{x}</b><br>Score: %{y}/100<extra></extra>',
  }] : [];

  const statusPie = ipos.length ? [{
    type: 'pie',
    labels: ['Open', 'Upcoming', 'Closed', 'Unknown'],
    values: [
      ipos.filter(i => i.status === 'Open').length,
      ipos.filter(i => i.status === 'Upcoming').length,
      ipos.filter(i => i.status === 'Closed').length,
      ipos.filter(i => i.status === 'Unknown').length,
    ],
    marker: { colors: ['#00ff88', '#00d4ff', '#8b949e', '#ffa502'],
      line: { color: '#060910', width: 2 } },
    hole: 0.5,
    textinfo: 'label+value',
    textfont: { color: '#f0f6fc', size: 11 },
    hovertemplate: '<b>%{label}</b><br>%{value} IPOs<extra></extra>',
  }] : [];

  const catBar = ipos.length ? (() => {
    const cats = {};
    ipos.forEach(i => { cats[i.category] = (cats[i.category] || 0) + 1; });
    return [{
      type: 'bar',
      x: Object.keys(cats),
      y: Object.values(cats),
      marker: { color: ['#00d4ff', '#a855f7', '#ffa502', '#00ff88'] },
      text: Object.values(cats).map(v => v + ' IPOs'),
      textposition: 'outside',
      hovertemplate: '<b>%{x}</b><br>%{y} IPOs<extra></extra>',
    }];
  })() : [];

  const recBar = ipos.length ? (() => {
    const apply   = ipos.filter(i => i.recommendation === 'APPLY').length;
    const neutral = ipos.filter(i => i.recommendation === 'NEUTRAL').length;
    const avoid   = ipos.filter(i => i.recommendation === 'AVOID').length;
    return [{
      type: 'bar',
      x: ['APPLY', 'NEUTRAL', 'AVOID'],
      y: [apply, neutral, avoid],
      marker: { color: ['rgba(0,255,136,0.75)', 'rgba(255,165,2,0.75)', 'rgba(255,71,87,0.75)'] },
      text: [apply, neutral, avoid].map(v => v + ' IPOs'),
      textposition: 'outside',
      hovertemplate: '<b>%{x}</b><br>%{y} IPOs<extra></extra>',
    }];
  })() : [];

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div className="section-title">🚀 IPO Intelligence Hub</div>
        <div className="section-subtitle">
          <span className="pulse-dot" />
          Live data from ipowatch.in · Real multi-factor scoring · Click any card for details
          <button className="btn btn-secondary"
            style={{ marginLeft: 'auto', padding: '5px 12px', fontSize: '0.75rem' }}
            onClick={load}>🔄 Refresh</button>
        </div>
      </div>

      {loading && (
        <div className="loading">
          <div className="spinner" />
          <div className="loading-text">Fetching live IPO data from ipowatch.in...</div>
        </div>
      )}

      {!loading && data && (
        <>
          {/* KPI row */}
          <div className="grid-4" style={{ marginBottom: '1.25rem' }}>
            {[
              { label: 'Total IPOs',  val: data.total,          color: 'var(--accent)' },
              { label: '🟢 Open Now', val: data.open_count,     color: '#00ff88' },
              { label: '🔵 Upcoming', val: data.upcoming_count, color: '#00d4ff' },
              { label: '⚫ Closed',   val: data.closed_count,   color: '#8b949e' },
            ].map(k => (
              <div key={k.label} className="kpi-card" style={{ borderLeftColor: k.color }}>
                <div className="kpi-label">{k.label}</div>
                <div className="kpi-value" style={{ color: k.color, fontSize: '2rem' }}>{k.val}</div>
              </div>
            ))}
          </div>

          {/* Filter + View toggle */}
          <div style={{ display: 'flex', gap: 8, marginBottom: '1.25rem',
            flexWrap: 'wrap', alignItems: 'center' }}>
            {['All', 'Open', 'Upcoming', 'Closed'].map(f => (
              <button key={f}
                className={'btn ' + (filter === f ? 'btn-primary' : 'btn-secondary')}
                style={{ padding: '6px 16px', fontSize: '0.8rem' }}
                onClick={() => setFilter(f)}>
                {f === 'Open' ? '🟢' : f === 'Upcoming' ? '🔵' : f === 'Closed' ? '⚫' : '📋'} {f}
                {' '}
                <span style={{ opacity: 0.7, fontSize: '0.72rem' }}>
                  ({f === 'All' ? ipos.length :
                    ipos.filter(i => i.status === f).length})
                </span>
              </button>
            ))}
            <div style={{ marginLeft: 'auto', display: 'flex', gap: 4 }}>
              {[['cards', '🃏 Cards'], ['charts', '📊 Charts']].map(([id, label]) => (
                <button key={id}
                  className={'btn ' + (view === id ? 'btn-primary' : 'btn-secondary')}
                  style={{ padding: '6px 14px', fontSize: '0.78rem' }}
                  onClick={() => setView(id)}>{label}</button>
              ))}
            </div>
          </div>

          {/* Cards view */}
          {view === 'cards' && (
            <>
              {filtered.length === 0 && (
                <div className="card" style={{ textAlign: 'center',
                  color: 'var(--text-secondary)', padding: '3rem' }}>
                  <div style={{ fontSize: '2rem', marginBottom: '0.75rem' }}>📭</div>
                  No IPOs found for this filter.
                </div>
              )}
              <div className="grid-3">
                {filtered.map((item, i) => <IPOCard key={i} item={item} />)}
              </div>
            </>
          )}

          {/* Charts view */}
          {view === 'charts' && ipos.length > 0 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {/* Row 1 */}
              <div className="grid-2">
                <div className="card">
                  <PlotlyChart data={statusPie}
                    layout={{
                      title: 'IPO Status Distribution',
                      height: 360, showlegend: true,
                      annotations: [{
                        text: '<b>' + ipos.length + '</b><br>total',
                        x: 0.5, y: 0.5, showarrow: false,
                        font: { color: '#f0f6fc', size: 14 },
                      }],
                    }} />
                </div>
                <div className="card">
                  <PlotlyChart data={recBar}
                    layout={{
                      title: 'Recommendation Distribution',
                      height: 360,
                      yaxis: { title: 'Number of IPOs' },
                      bargap: 0.4,
                    }} />
                </div>
              </div>

              {/* Row 2 — Score bar (full width) */}
              <div className="card">
                <PlotlyChart data={scoreBar}
                  layout={{
                    title: 'IPO Scores — Top 15 (Green ≥65 = Apply, Orange = Neutral, Red = Avoid)',
                    height: 420,
                    yaxis: { title: 'Score /100', range: [0, 115] },
                    xaxis: { tickangle: -30 },
                    shapes: [
                      { type: 'line', x0: -0.5, x1: 14.5, y0: 65, y1: 65,
                        line: { color: 'rgba(0,255,136,0.4)', dash: 'dot', width: 1.5 } },
                      { type: 'line', x0: -0.5, x1: 14.5, y0: 45, y1: 45,
                        line: { color: 'rgba(255,71,87,0.4)', dash: 'dot', width: 1.5 } },
                    ],
                    annotations: [
                      { x: 14.5, y: 65, text: 'APPLY threshold', showarrow: false,
                        font: { color: '#00ff88', size: 10 }, xanchor: 'right' },
                      { x: 14.5, y: 45, text: 'AVOID threshold', showarrow: false,
                        font: { color: '#ff4757', size: 10 }, xanchor: 'right' },
                    ],
                  }} />
              </div>

              {/* Row 3 */}
              <div className="card">
                <PlotlyChart data={catBar}
                  layout={{
                    title: 'IPOs by Category (Mainboard vs SME)',
                    height: 320,
                    yaxis: { title: 'Number of IPOs' },
                    bargap: 0.4,
                  }} />
              </div>

              {/* Data table */}
              <div className="card">
                <div style={{ fontWeight: 600, color: 'var(--accent)', marginBottom: '0.75rem' }}>
                  📋 Complete IPO Data Table
                </div>
                <div className="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        {['Company', 'Status', 'Category', 'Open Date', 'Close Date',
                          'Price Band', 'Issue Size', 'Score', 'Recommendation'].map(h => (
                          <th key={h}>{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {ipos.map((item, i) => {
                        const rc = REC_C[item.recommendation] || '#ffa502';
                        const sc = C[item.status] || '#8b949e';
                        return (
                          <tr key={i}>
                            <td style={{ fontWeight: 600, maxWidth: 180 }}>{item.name}</td>
                            <td><StatusPill status={item.status} /></td>
                            <td>
                              <span className="badge badge-purple" style={{ fontSize: '0.65rem' }}>
                                {item.category}
                              </span>
                            </td>
                            <td style={{ fontSize: '0.8rem' }}>{item.open_date}</td>
                            <td style={{ fontSize: '0.8rem' }}>{item.close_date}</td>
                            <td style={{ fontSize: '0.8rem' }}>{item.price_band}</td>
                            <td style={{ fontSize: '0.8rem' }}>{item.issue_size}</td>
                            <td>
                              <span style={{ fontWeight: 800,
                                color: item.score >= 65 ? '#00ff88' : item.score >= 45 ? '#ffa502' : '#ff4757' }}>
                                {item.score}/100
                              </span>
                            </td>
                            <td>
                              <span style={{ color: rc, fontWeight: 700, fontSize: '0.8rem' }}>
                                {REC_ICON[item.recommendation]} {item.recommendation}
                              </span>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Source note */}
          <div style={{ marginTop: '1rem', fontSize: '0.7rem', color: '#484f58', textAlign: 'center' }}>
            Data source: ipowatch.in (live) · Scoring: Issue size + Category + Subscription + GMP + Status
            · Last fetched: {new Date(data.timestamp).toLocaleTimeString('en-IN')}
          </div>
        </>
      )}
    </div>
  );
}
