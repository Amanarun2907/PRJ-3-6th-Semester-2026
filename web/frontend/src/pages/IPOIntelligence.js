import React, { useEffect, useState, useCallback } from 'react';
import { ipo } from '../api';
import PlotlyChart from '../components/PlotlyChart';
import toast from 'react-hot-toast';

const C = { Open:'#00ff88', Upcoming:'#00d4ff', Closed:'#8b949e', Unknown:'#ffa502' };
const RC = { APPLY:'#00ff88', AVOID:'#ff4757', NEUTRAL:'#ffa502' };
const RI = { APPLY:'✅', AVOID:'❌', NEUTRAL:'⚠️' };

/* ── Score Ring ── */
function ScoreRing({ score, size = 72 }) {
  const color = score >= 65 ? '#00ff88' : score >= 45 ? '#ffa502' : '#ff4757';
  const r = size / 2 - 5;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  return (
    <div style={{ position:'relative', width:size, height:size, flexShrink:0 }}>
      <svg width={size} height={size} style={{ transform:'rotate(-90deg)' }}>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="#21262d" strokeWidth="5"/>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth="5"
          strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
          style={{ transition:'stroke-dasharray 0.8s ease' }}/>
      </svg>
      <div style={{ position:'absolute', inset:0, display:'flex',
        flexDirection:'column', alignItems:'center', justifyContent:'center' }}>
        <div style={{ fontSize: size > 60 ? '1rem' : '0.75rem',
          fontWeight:900, color, lineHeight:1 }}>{score}</div>
        <div style={{ fontSize:'0.5rem', color:'#8b949e' }}>/100</div>
      </div>
    </div>
  );
}

/* ── Status Pill ── */
function StatusPill({ status }) {
  const color = C[status] || '#8b949e';
  return (
    <span style={{ background:`${color}18`, color, border:`1px solid ${color}44`,
      borderRadius:20, padding:'3px 10px', fontSize:'0.72rem', fontWeight:700,
      display:'inline-flex', alignItems:'center', gap:4 }}>
      <span style={{ width:6, height:6, borderRadius:'50%', background:color,
        animation: status==='Open' ? 'pulse 1.5s infinite' : 'none' }}/>
      {status}
    </span>
  );
}

/* ── Rec Badge ── */
function RecBadge({ rec, large }) {
  const c = RC[rec] || '#ffa502';
  return (
    <span style={{ background:`${c}15`, color:c, border:`1px solid ${c}33`,
      borderRadius:8, padding: large ? '8px 24px' : '4px 14px',
      fontWeight:800, fontSize: large ? '0.95rem' : '0.78rem',
      letterSpacing:'0.05em' }}>
      {RI[rec]} {rec}
    </span>
  );
}

/* ── IPO Detail Modal ── */
function IPODetailModal({ ipoItem, onClose }) {
  const [detail,   setDetail]   = useState(null);
  const [aiLoading,setAiLoading]= useState(false);
  const [aiDone,   setAiDone]   = useState(false);

  useEffect(() => {
    if (!ipoItem?.detail_url) return;
    ipo.aiAnalysis(ipoItem.detail_url, ipoItem.name)
      .then(r => setDetail(r.data))
      .catch(() => setDetail(ipoItem));
  }, [ipoItem]);

  if (!ipoItem) return null;
  const d = detail || ipoItem;
  const color = C[d.status] || '#8b949e';
  const rc    = RC[d.recommendation] || '#ffa502';

  /* Financials chart */
  const finChart = d.financials?.length > 1 ? (() => {
    const rows = d.financials.filter(r => r[0] !== 'Period Ended' && r[0] !== 'Particular');
    const labels = rows.map(r => r[0]);
    const revenue = rows.map(r => parseFloat(r[1]?.replace(/[₹,]/g,'')) || 0);
    const pat     = rows.map(r => parseFloat(r[3]?.replace(/[₹,]/g,'')) || 0);
    return [
      { type:'bar', name:'Revenue (Cr)', x:labels, y:revenue,
        marker:{color:'rgba(0,212,255,0.7)'}, hovertemplate:'%{x}<br>Revenue: ₹%{y}Cr<extra></extra>' },
      { type:'bar', name:'PAT (Cr)', x:labels, y:pat,
        marker:{color:'rgba(0,255,136,0.7)'}, hovertemplate:'%{x}<br>PAT: ₹%{y}Cr<extra></extra>' },
    ];
  })() : null;

  /* Score breakdown radar */
  const radarData = [{
    type:'scatterpolar', fill:'toself',
    r: [
      Math.min(100, parseFloat(d.roe) || 0),
      Math.min(100, parseFloat(d.pat_margin) || 0),
      Math.min(100, parseFloat(d.ebitda_margin) || 0),
      d.status === 'Open' ? 80 : d.status === 'Upcoming' ? 60 : 40,
      d.category?.toUpperCase().includes('MAIN') ? 80 : 50,
    ],
    theta: ['ROE %', 'PAT Margin', 'EBITDA Margin', 'Timing', 'Category'],
    line: { color: rc },
    fillcolor: `${rc}20`,
    name: d.name?.slice(0,20),
  }];

  return (
    <div style={{ position:'fixed', inset:0, background:'rgba(0,0,0,0.85)',
      zIndex:1000, display:'flex', alignItems:'flex-start', justifyContent:'center',
      padding:'1.5rem', overflowY:'auto' }}
      onClick={e => e.target === e.currentTarget && onClose()}>
      <div style={{ background:'#111827', border:`1px solid ${color}`,
        borderRadius:16, width:'100%', maxWidth:900, padding:'1.75rem',
        position:'relative' }}>

        {/* Close */}
        <button onClick={onClose} style={{ position:'absolute', top:16, right:16,
          background:'var(--bg-hover)', border:'1px solid var(--border)',
          borderRadius:8, color:'var(--text-secondary)', cursor:'pointer',
          padding:'4px 10px', fontSize:'0.85rem' }}>✕ Close</button>

        {/* Header */}
        <div style={{ display:'flex', gap:16, alignItems:'flex-start',
          marginBottom:'1.25rem', paddingRight:60 }}>
          <ScoreRing score={d.score || 50} size={80}/>
          <div style={{ flex:1 }}>
            <div style={{ fontWeight:900, fontSize:'1.2rem', color:'var(--text-primary)',
              marginBottom:6 }}>{d.name}</div>
            <div style={{ display:'flex', gap:8, flexWrap:'wrap', marginBottom:8 }}>
              <StatusPill status={d.status}/>
              <span className="badge badge-purple" style={{ fontSize:'0.68rem' }}>
                {d.category}
              </span>
              <RecBadge rec={d.recommendation}/>
            </div>
            <div style={{ display:'flex', gap:20, flexWrap:'wrap', fontSize:'0.82rem' }}>
              {[
                { label:'Price Band',    val: d.price_band || d.price_band || 'N/A' },
                { label:'Issue Size',    val: d.issue_size_full || d.issue_size || 'N/A' },
                { label:'Lot Size',      val: d.lot_size ? `${d.lot_size} lots` : 'N/A' },
                { label:'Min Investment',val: d.min_investment || 'N/A' },
                { label:'Listing Date',  val: d.listing_date || 'N/A' },
              ].map(f => (
                <div key={f.label}>
                  <div style={{ fontSize:'0.65rem', color:'var(--text-secondary)',
                    textTransform:'uppercase', letterSpacing:'0.04em' }}>{f.label}</div>
                  <div style={{ fontWeight:600, color:'var(--accent)' }}>{f.val}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {!detail && (
          <div className="loading" style={{ padding:'1rem' }}>
            <div className="spinner-sm"/>
            <span style={{ fontSize:'0.82rem' }}>Loading detailed analysis...</span>
          </div>
        )}

        {detail && (
          <>
            {/* Key dates */}
            <div className="grid-4" style={{ marginBottom:'1.25rem' }}>
              {[
                { label:'Open Date',       val: d.open_date_full  || d.open_date  || 'N/A' },
                { label:'Close Date',      val: d.close_date_full || d.close_date || 'N/A' },
                { label:'Allotment',       val: d.allotment_date  || 'N/A' },
                { label:'Listing Date',    val: d.listing_date    || 'N/A' },
              ].map(f => (
                <div key={f.label} style={{ background:'var(--bg-secondary)',
                  borderRadius:10, padding:'0.75rem', textAlign:'center' }}>
                  <div style={{ fontSize:'0.65rem', color:'var(--text-secondary)',
                    textTransform:'uppercase', letterSpacing:'0.04em', marginBottom:3 }}>
                    {f.label}
                  </div>
                  <div style={{ fontWeight:700, color:'var(--accent)', fontSize:'0.85rem' }}>
                    {f.val}
                  </div>
                </div>
              ))}
            </div>

            {/* Financial KPIs */}
            {(d.roe || d.pat_margin || d.ebitda_margin) && (
              <div style={{ marginBottom:'1.25rem' }}>
                <div style={{ fontWeight:700, color:'var(--accent)', marginBottom:'0.75rem',
                  fontSize:'0.9rem' }}>📊 Financial KPIs</div>
                <div className="grid-5">
                  {[
                    { label:'ROE',          val: d.roe          || 'N/A', good: v => parseFloat(v) > 15 },
                    { label:'ROCE',         val: d.roce         || 'N/A', good: v => parseFloat(v) > 15 },
                    { label:'EBITDA Margin',val: d.ebitda_margin|| 'N/A', good: v => parseFloat(v) > 10 },
                    { label:'PAT Margin',   val: d.pat_margin   || 'N/A', good: v => parseFloat(v) > 8  },
                    { label:'Debt/Equity',  val: d.debt_equity  || 'N/A', good: v => parseFloat(v) < 1  },
                  ].map(f => {
                    const isGood = f.good && f.val !== 'N/A' ? f.good(f.val) : null;
                    const c = isGood === true ? '#00ff88' : isGood === false ? '#ff4757' : 'var(--accent)';
                    return (
                      <div key={f.label} style={{ background:'var(--bg-secondary)',
                        borderRadius:10, padding:'0.75rem', textAlign:'center',
                        borderBottom:`2px solid ${c}` }}>
                        <div style={{ fontSize:'0.65rem', color:'var(--text-secondary)',
                          marginBottom:3, textTransform:'uppercase', letterSpacing:'0.04em' }}>
                          {f.label}
                        </div>
                        <div style={{ fontWeight:800, color:c, fontSize:'1rem' }}>{f.val}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Promoter holding */}
            {(d.promoter_pre || d.promoter_post) && (
              <div style={{ marginBottom:'1.25rem' }}>
                <div style={{ fontWeight:700, color:'var(--accent)', marginBottom:'0.75rem',
                  fontSize:'0.9rem' }}>👥 Promoter Holding</div>
                <div className="grid-2">
                  {[
                    { label:'Pre-Issue', val: d.promoter_pre  || 'N/A', color:'#00d4ff' },
                    { label:'Post-Issue',val: d.promoter_post || 'N/A', color:'#00ff88' },
                  ].map(f => (
                    <div key={f.label} style={{ background:'var(--bg-secondary)',
                      borderRadius:10, padding:'1rem', textAlign:'center' }}>
                      <div style={{ fontSize:'0.72rem', color:'var(--text-secondary)',
                        marginBottom:4 }}>{f.label} Promoter Holding</div>
                      <div style={{ fontWeight:900, color:f.color, fontSize:'1.4rem' }}>
                        {f.val}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Charts row */}
            <div className={finChart ? 'grid-2' : ''} style={{ marginBottom:'1.25rem' }}>
              {finChart && (
                <div className="card" style={{ padding:'0.75rem' }}>
                  <PlotlyChart data={finChart}
                    layout={{ title:'Revenue & PAT History (₹ Cr)', height:280,
                      barmode:'group', yaxis:{title:'₹ Crores'},
                      margin:{l:40,r:10,t:40,b:40} }}/>
                </div>
              )}
              <div className="card" style={{ padding:'0.75rem' }}>
                <PlotlyChart data={radarData}
                  layout={{ title:'IPO Quality Radar', height:280,
                    polar:{ radialaxis:{ range:[0,100], visible:true } },
                    margin:{l:20,r:20,t:40,b:20} }}/>
              </div>
            </div>

            {/* Peer comparison */}
            {d.peers?.length > 0 && (
              <div style={{ marginBottom:'1.25rem' }}>
                <div style={{ fontWeight:700, color:'var(--accent)', marginBottom:'0.75rem',
                  fontSize:'0.9rem' }}>🏭 Peer Comparison</div>
                <div style={{ overflowX:'auto', borderRadius:10,
                  border:'1px solid var(--border)' }}>
                  <table>
                    <thead>
                      <tr>
                        {['Company','EPS','P/E Ratio','RoNW %'].map(h=><th key={h}>{h}</th>)}
                      </tr>
                    </thead>
                    <tbody>
                      {d.peers.map((p,i) => (
                        <tr key={i}>
                          <td style={{ fontWeight:600 }}>{p.company}</td>
                          <td style={{ color:'var(--accent)' }}>{p.eps}</td>
                          <td style={{ color:'var(--accent-orange)' }}>{p.pe}</td>
                          <td style={{ color:'var(--accent-green)' }}>{p.ronw}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Objects of issue */}
            {d.objects_of_issue?.length > 0 && (
              <div style={{ marginBottom:'1.25rem' }}>
                <div style={{ fontWeight:700, color:'var(--accent)', marginBottom:'0.75rem',
                  fontSize:'0.9rem' }}>💰 Use of IPO Proceeds</div>
                <div style={{ display:'flex', flexDirection:'column', gap:6 }}>
                  {d.objects_of_issue.map((o,i) => (
                    <div key={i} style={{ display:'flex', justifyContent:'space-between',
                      padding:'8px 12px', background:'var(--bg-secondary)', borderRadius:8,
                      fontSize:'0.82rem' }}>
                      <span style={{ color:'var(--text-secondary)' }}>{o.purpose}</span>
                      <span style={{ fontWeight:600, color:'var(--accent)' }}>{o.amount}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* AI Analysis */}
            {d.ai_analysis ? (
              <div style={{ background:'linear-gradient(135deg,rgba(168,85,247,0.08),rgba(0,212,255,0.04))',
                border:'1px solid rgba(168,85,247,0.3)', borderRadius:12, padding:'1.25rem' }}>
                <div style={{ fontWeight:700, color:'#a855f7', marginBottom:'0.75rem',
                  display:'flex', alignItems:'center', gap:8 }}>
                  🤖 AI Analysis — Groq Llama 3.3 70B
                  <span className="badge badge-purple" style={{ fontSize:'0.65rem' }}>
                    Live Analysis
                  </span>
                </div>
                <div style={{ color:'var(--text-primary)', lineHeight:1.85,
                  fontSize:'0.875rem', whiteSpace:'pre-wrap' }}>
                  {d.ai_analysis}
                </div>
              </div>
            ) : (
              <div className="info-box">
                ℹ️ AI analysis requires GROQ_API_KEY in .env
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

/* ── Main Page ── */
export default function IPOIntelligence() {
  const [data,      setData]      = useState(null);
  const [loading,   setLoading]   = useState(true);
  const [filter,    setFilter]    = useState('All');
  const [view,      setView]      = useState('cards');
  const [selected,  setSelected]  = useState(null);
  const [sortBy,    setSortBy]    = useState('status');

  const load = useCallback(() => {
    setLoading(true);
    ipo.live()
      .then(r => setData(r.data))
      .catch(() => toast.error('Failed to fetch IPO data'))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const ipos = data?.ipos || [];

  /* Sort */
  const sorted = [...ipos].sort((a, b) => {
    if (sortBy === 'score')  return b.score - a.score;
    if (sortBy === 'size')   return (parseFloat(b.issue_size) || 0) - (parseFloat(a.issue_size) || 0);
    const order = { Open:0, Upcoming:1, Closed:2, Unknown:3 };
    return (order[a.status] || 3) - (order[b.status] || 3);
  });
  const filtered = filter === 'All' ? sorted : sorted.filter(i => i.status === filter);

  /* ── Analytics charts ── */
  const scoreBar = ipos.slice(0,15).length ? [{
    type:'bar',
    x: ipos.slice(0,15).map(i => i.name?.slice(0,16) + (i.name?.length>16?'…':'')),
    y: ipos.slice(0,15).map(i => i.score),
    marker:{ color: ipos.slice(0,15).map(i =>
      i.score>=65?'rgba(0,255,136,0.8)':i.score>=45?'rgba(255,165,2,0.8)':'rgba(255,71,87,0.8)'),
      line:{ color: ipos.slice(0,15).map(i =>
        i.score>=65?'#00ff88':i.score>=45?'#ffa502':'#ff4757'), width:1 } },
    text: ipos.slice(0,15).map(i => i.score+'/100'),
    textposition:'outside', textfont:{size:10},
    hovertemplate:'<b>%{x}</b><br>Score: %{y}/100<extra></extra>',
  }] : [];

  const statusPie = ipos.length ? [{
    type:'pie',
    labels:['Open','Upcoming','Closed','Unknown'],
    values:[
      ipos.filter(i=>i.status==='Open').length,
      ipos.filter(i=>i.status==='Upcoming').length,
      ipos.filter(i=>i.status==='Closed').length,
      ipos.filter(i=>i.status==='Unknown').length,
    ],
    marker:{ colors:['#00ff88','#00d4ff','#8b949e','#ffa502'],
      line:{color:'#060910',width:2} },
    hole:0.5, textinfo:'label+value',
    textfont:{color:'#f0f6fc',size:11},
    hovertemplate:'<b>%{label}</b><br>%{value} IPOs<extra></extra>',
  }] : [];

  const recPie = ipos.length ? [{
    type:'pie',
    labels:['APPLY','NEUTRAL','AVOID'],
    values:[
      ipos.filter(i=>i.recommendation==='APPLY').length,
      ipos.filter(i=>i.recommendation==='NEUTRAL').length,
      ipos.filter(i=>i.recommendation==='AVOID').length,
    ],
    marker:{ colors:['#00ff88','#ffa502','#ff4757'],
      line:{color:'#060910',width:2} },
    hole:0.5, textinfo:'label+value',
    textfont:{color:'#f0f6fc',size:11},
    hovertemplate:'<b>%{label}</b><br>%{value} IPOs<extra></extra>',
  }] : [];

  const catBar = ipos.length ? (() => {
    const cats = {};
    ipos.forEach(i => { cats[i.category] = (cats[i.category]||0)+1; });
    return [{
      type:'bar', x:Object.keys(cats), y:Object.values(cats),
      marker:{color:['#00d4ff','#a855f7','#ffa502','#00ff88']},
      text:Object.values(cats).map(v=>v+' IPOs'), textposition:'outside',
      hovertemplate:'<b>%{x}</b><br>%{y} IPOs<extra></extra>',
    }];
  })() : [];

  /* Score distribution histogram */
  const scoreHist = ipos.length ? [{
    type:'histogram', x: ipos.map(i=>i.score),
    marker:{ color:'rgba(0,212,255,0.6)', line:{color:'#00d4ff',width:1} },
    nbinsx:10,
    hovertemplate:'Score range: %{x}<br>Count: %{y}<extra></extra>',
  }] : [];

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div className="section-title">🚀 IPO Intelligence Hub</div>
        <div className="section-subtitle">
          <span className="pulse-dot"/>
          Live data from ipowatch.in · Real multi-factor scoring · AI analysis per IPO
          · Click any card for deep analysis
          <button className="btn btn-secondary"
            style={{ marginLeft:'auto', padding:'5px 12px', fontSize:'0.75rem' }}
            onClick={load}>🔄 Refresh</button>
        </div>
      </div>

      {loading && (
        <div className="loading">
          <div className="spinner"/>
          <div className="loading-text">Fetching live IPO data from ipowatch.in...</div>
        </div>
      )}

      {!loading && data && (
        <>
          {/* KPI row */}
          <div className="grid-5" style={{ marginBottom:'1.25rem' }}>
            {[
              { label:'Total IPOs',  val:data.total,          color:'var(--accent)' },
              { label:'🟢 Open Now', val:data.open_count,     color:'#00ff88' },
              { label:'🔵 Upcoming', val:data.upcoming_count, color:'#00d4ff' },
              { label:'⚫ Closed',   val:data.closed_count,   color:'#8b949e' },
              { label:'✅ Apply',    val:ipos.filter(i=>i.recommendation==='APPLY').length, color:'#00ff88' },
            ].map(k => (
              <div key={k.label} className="kpi-card" style={{ borderLeftColor:k.color }}>
                <div className="kpi-label">{k.label}</div>
                <div className="kpi-value" style={{ color:k.color, fontSize:'2rem' }}>{k.val}</div>
              </div>
            ))}
          </div>

          {/* Controls */}
          <div style={{ display:'flex', gap:8, marginBottom:'1.25rem',
            flexWrap:'wrap', alignItems:'center' }}>
            {/* Status filter */}
            {['All','Open','Upcoming','Closed'].map(f => (
              <button key={f}
                className={'btn '+(filter===f?'btn-primary':'btn-secondary')}
                style={{ padding:'6px 14px', fontSize:'0.8rem' }}
                onClick={() => setFilter(f)}>
                {f==='Open'?'🟢':f==='Upcoming'?'🔵':f==='Closed'?'⚫':'📋'} {f}
                {' '}({f==='All'?ipos.length:ipos.filter(i=>i.status===f).length})
              </button>
            ))}
            {/* Sort */}
            <div style={{ marginLeft:8, display:'flex', alignItems:'center', gap:6 }}>
              <span style={{ fontSize:'0.75rem', color:'var(--text-secondary)' }}>Sort:</span>
              {[['status','Status'],['score','Score'],['size','Size']].map(([id,label]) => (
                <button key={id}
                  className={'btn '+(sortBy===id?'btn-primary':'btn-secondary')}
                  style={{ padding:'5px 10px', fontSize:'0.75rem' }}
                  onClick={() => setSortBy(id)}>{label}</button>
              ))}
            </div>
            {/* View toggle */}
            <div style={{ marginLeft:'auto', display:'flex', gap:4 }}>
              {[['cards','🃏 Cards'],['analytics','📊 Analytics']].map(([id,label]) => (
                <button key={id}
                  className={'btn '+(view===id?'btn-primary':'btn-secondary')}
                  style={{ padding:'6px 12px', fontSize:'0.78rem' }}
                  onClick={() => setView(id)}>{label}</button>
              ))}
            </div>
          </div>

          {/* ── CARDS VIEW ── */}
          {view === 'cards' && (
            <>
              {filtered.length === 0 && (
                <div className="card" style={{ textAlign:'center',
                  color:'var(--text-secondary)', padding:'3rem' }}>
                  <div style={{ fontSize:'2rem', marginBottom:'0.75rem' }}>📭</div>
                  No IPOs found for this filter.
                </div>
              )}
              <div className="grid-3">
                {filtered.map((item, i) => {
                  const sc = C[item.status] || '#8b949e';
                  const rc = RC[item.recommendation] || '#ffa502';
                  return (
                    <div key={i} className="card"
                      style={{ borderTop:`3px solid ${sc}`, cursor:'pointer',
                        transition:'all 0.2s' }}
                      onClick={() => setSelected(item)}
                      onMouseEnter={e => e.currentTarget.style.transform='translateY(-3px)'}
                      onMouseLeave={e => e.currentTarget.style.transform='none'}>

                      {/* Top row */}
                      <div style={{ display:'flex', justifyContent:'space-between',
                        alignItems:'flex-start', gap:8, marginBottom:10 }}>
                        <div style={{ flex:1 }}>
                          <div style={{ fontWeight:700, fontSize:'0.9rem',
                            lineHeight:1.3, marginBottom:6 }}>{item.name}</div>
                          <div style={{ display:'flex', gap:6, flexWrap:'wrap' }}>
                            <StatusPill status={item.status}/>
                            <span style={{ background:'rgba(168,85,247,0.12)',
                              color:'#a855f7', border:'1px solid rgba(168,85,247,0.25)',
                              borderRadius:20, padding:'3px 8px',
                              fontSize:'0.65rem', fontWeight:600 }}>
                              {item.category}
                            </span>
                          </div>
                        </div>
                        <ScoreRing score={item.score||50} size={60}/>
                      </div>

                      {/* Data grid */}
                      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr',
                        gap:'5px 12px', fontSize:'0.78rem', marginBottom:10 }}>
                        {[
                          { label:'Price Band',  val:item.price_band  || 'TBA' },
                          { label:'Issue Size',  val:item.issue_size  || 'N/A' },
                          { label:'Open Date',   val:item.open_date   || 'N/A' },
                          { label:'Close Date',  val:item.close_date  || 'N/A' },
                        ].map(r => (
                          <div key={r.label}>
                            <div style={{ color:'#8b949e', fontSize:'0.65rem',
                              marginBottom:1, textTransform:'uppercase',
                              letterSpacing:'0.04em' }}>{r.label}</div>
                            <div style={{ fontWeight:500 }}>{r.val}</div>
                          </div>
                        ))}
                      </div>

                      {/* Score bar */}
                      <div style={{ marginBottom:10 }}>
                        <div style={{ display:'flex', justifyContent:'space-between',
                          fontSize:'0.68rem', marginBottom:3 }}>
                          <span style={{ color:'#8b949e' }}>IPO Score</span>
                          <span style={{ color:rc, fontWeight:700 }}>
                            {item.score}/100
                          </span>
                        </div>
                        <div style={{ background:'#21262d', borderRadius:4, height:5 }}>
                          <div style={{ width:`${item.score}%`, height:'100%',
                            background:`linear-gradient(90deg,${rc},${rc}aa)`,
                            borderRadius:4, transition:'width 0.6s ease' }}/>
                        </div>
                      </div>

                      {/* Recommendation + CTA */}
                      <div style={{ display:'flex', justifyContent:'space-between',
                        alignItems:'center' }}>
                        <RecBadge rec={item.recommendation}/>
                        <span style={{ fontSize:'0.68rem', color:'#484f58' }}>
                          Click for AI analysis →
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </>
          )}

          {/* ── ANALYTICS VIEW ── */}
          {view === 'analytics' && ipos.length > 0 && (
            <div style={{ display:'flex', flexDirection:'column', gap:'1rem' }}>
              {/* Row 1 */}
              <div className="grid-3">
                <div className="card">
                  <PlotlyChart data={statusPie}
                    layout={{ title:'IPO Status Distribution', height:320,
                      showlegend:true,
                      annotations:[{ text:`<b>${ipos.length}</b><br>total`,
                        x:0.5,y:0.5,showarrow:false,
                        font:{color:'#f0f6fc',size:13} }] }}/>
                </div>
                <div className="card">
                  <PlotlyChart data={recPie}
                    layout={{ title:'Recommendation Distribution', height:320,
                      showlegend:true,
                      annotations:[{ text:'<b>AI</b><br>Recs',
                        x:0.5,y:0.5,showarrow:false,
                        font:{color:'#f0f6fc',size:13} }] }}/>
                </div>
                <div className="card">
                  <PlotlyChart data={catBar}
                    layout={{ title:'IPOs by Category', height:320,
                      yaxis:{title:'Count'}, bargap:0.4 }}/>
                </div>
              </div>

              {/* Score bar — full width */}
              <div className="card">
                <PlotlyChart data={scoreBar}
                  layout={{ title:'IPO Scores — Top 15 (Green ≥65 APPLY · Orange NEUTRAL · Red AVOID)',
                    height:420,
                    yaxis:{title:'Score /100', range:[0,115]},
                    xaxis:{tickangle:-30},
                    shapes:[
                      { type:'line',x0:-0.5,x1:14.5,y0:65,y1:65,
                        line:{color:'rgba(0,255,136,0.5)',dash:'dot',width:2} },
                      { type:'rect',x0:-0.5,x1:14.5,y0:65,y1:115,
                        fillcolor:'rgba(0,255,136,0.03)',line:{width:0} },
                      { type:'line',x0:-0.5,x1:14.5,y0:45,y1:45,
                        line:{color:'rgba(255,71,87,0.5)',dash:'dot',width:2} },
                      { type:'rect',x0:-0.5,x1:14.5,y0:0,y1:45,
                        fillcolor:'rgba(255,71,87,0.03)',line:{width:0} },
                    ],
                    annotations:[
                      { x:14.5,y:65,text:'APPLY threshold',showarrow:false,
                        font:{color:'#00ff88',size:10},xanchor:'right' },
                      { x:14.5,y:45,text:'AVOID threshold',showarrow:false,
                        font:{color:'#ff4757',size:10},xanchor:'right' },
                    ] }}/>
              </div>

              {/* Score histogram */}
              <div className="grid-2">
                <div className="card">
                  <PlotlyChart data={scoreHist}
                    layout={{ title:'Score Distribution Histogram', height:320,
                      xaxis:{title:'IPO Score'},
                      yaxis:{title:'Number of IPOs'} }}/>
                </div>
                {/* Summary table */}
                <div className="card">
                  <div style={{ fontWeight:600, color:'var(--accent)',
                    marginBottom:'0.75rem', fontSize:'0.9rem' }}>
                    📋 Quick Reference Table
                  </div>
                  <div style={{ overflowY:'auto', maxHeight:280 }}>
                    <table>
                      <thead>
                        <tr>
                          {['IPO','Status','Score','Rec'].map(h=><th key={h}>{h}</th>)}
                        </tr>
                      </thead>
                      <tbody>
                        {sorted.slice(0,20).map((item,i) => (
                          <tr key={i} style={{ cursor:'pointer' }}
                            onClick={() => { setSelected(item); setView('cards'); }}>
                            <td style={{ fontWeight:600, fontSize:'0.78rem',
                              maxWidth:160, overflow:'hidden',
                              textOverflow:'ellipsis', whiteSpace:'nowrap' }}>
                              {item.name}
                            </td>
                            <td><StatusPill status={item.status}/></td>
                            <td>
                              <span style={{ fontWeight:800,
                                color: item.score>=65?'#00ff88':item.score>=45?'#ffa502':'#ff4757' }}>
                                {item.score}
                              </span>
                            </td>
                            <td><RecBadge rec={item.recommendation}/></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Source note */}
          <div style={{ marginTop:'1rem', fontSize:'0.7rem',
            color:'#484f58', textAlign:'center' }}>
            Data: ipowatch.in (live) · Score: Issue size + Category + Subscription + GMP + Financials
            · Last fetched: {new Date(data.timestamp).toLocaleTimeString('en-IN')}
          </div>
        </>
      )}

      {/* Detail Modal */}
      {selected && (
        <IPODetailModal ipoItem={selected} onClose={() => setSelected(null)}/>
      )}
    </div>
  );
}
