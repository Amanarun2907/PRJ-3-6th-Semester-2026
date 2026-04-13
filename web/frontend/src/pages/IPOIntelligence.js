import React, { useEffect, useState, useCallback } from 'react';
import { ipo } from '../api';
import PlotlyChart from '../components/PlotlyChart';
import toast from 'react-hot-toast';

const C  = { Open:'#00ff88', Upcoming:'#00d4ff', Closed:'#8b949e', Unknown:'#ffa502' };
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
        <div style={{ fontSize: size > 60 ? '1rem' : '0.75rem', fontWeight:900, color, lineHeight:1 }}>
          {score}
        </div>
        <div style={{ fontSize:'0.5rem', color:'#8b949e' }}>/100</div>
      </div>
    </div>
  );
}

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

function RecBadge({ rec, large }) {
  const c = RC[rec] || '#ffa502';
  return (
    <span style={{ background:`${c}15`, color:c, border:`1px solid ${c}33`,
      borderRadius:8, padding: large ? '8px 24px' : '4px 14px',
      fontWeight:800, fontSize: large ? '0.95rem' : '0.78rem', letterSpacing:'0.05em' }}>
      {RI[rec]} {rec}
    </span>
  );
}

/* ── Exit Level Card ── */
function ExitCard({ label, price, pct, color, icon, sub }) {
  return (
    <div style={{ background:`${color}10`, border:`1px solid ${color}33`,
      borderRadius:12, padding:'0.9rem 1rem', textAlign:'center' }}>
      <div style={{ fontSize:'1.1rem', marginBottom:3 }}>{icon}</div>
      <div style={{ fontSize:'0.65rem', color:'#8b949e', textTransform:'uppercase',
        letterSpacing:'0.05em', marginBottom:4 }}>{label}</div>
      {price > 0 ? (
        <>
          <div style={{ fontWeight:900, color, fontSize:'1.2rem' }}>₹{price.toLocaleString('en-IN')}</div>
          <div style={{ fontSize:'0.75rem', color, fontWeight:700, marginTop:2 }}>
            {pct > 0 ? '+' : ''}{pct}%
          </div>
        </>
      ) : (
        <div style={{ fontWeight:700, color:'#8b949e', fontSize:'0.85rem' }}>TBA</div>
      )}
      {sub && <div style={{ fontSize:'0.65rem', color:'#484f58', marginTop:3 }}>{sub}</div>}
    </div>
  );
}
/* ── IPO Detail Modal ── */
function IPODetailModal({ ipoItem, onClose }) {
  const [detail, setDetail] = useState(null);
  const [tab, setTab] = useState('exit');

  useEffect(() => {
    if (!ipoItem?.detail_url) return;
    setDetail(null);
    ipo.aiAnalysis(ipoItem.detail_url, ipoItem.name)
      .then(r => setDetail(r.data))
      .catch(() => setDetail(ipoItem));
  }, [ipoItem]);

  if (!ipoItem) return null;
  const d = detail || ipoItem;
  const es = d.exit_strategy || {};
  const color = C[d.status] || '#8b949e';
  const rc = RC[d.recommendation] || '#ffa502';
  const ip = es.issue_price || 0;

  /* ── Exit timeline chart ── */
  const timelineChart = es.timeline && es.timeline.length > 0 && ip > 0 ? (() => {
    const days   = [0, 0, 1, 30, 90];
    const prices = [ip, es.stop_loss_price, es.listing_target_price, es.target_30d_price, es.target_90d_price];
    const labels = ['Issue Price', 'Stop Loss', 'Listing Target', '30-Day Target', '90-Day Target'];
    const colors = ['#00d4ff', '#ff4757', '#00ff88', '#ffa502', '#a855f7'];
    return [
      { type:'scatter', mode:'lines', name:'Price Path',
        x:[0,1,30,90], y:[ip, es.listing_target_price, es.target_30d_price, es.target_90d_price],
        line:{color:'rgba(0,212,255,0.3)', width:2, dash:'dot'}, hoverinfo:'skip' },
      { type:'scatter', mode:'markers+text', name:'Exit Levels',
        x:days, y:prices,
        text:labels.map((l,i) => l + '\n' + (prices[i] > 0 ? 'Rs.' + prices[i].toLocaleString('en-IN') : 'N/A')),
        textposition:['bottom center','top center','top center','top center','top center'],
        textfont:{size:10, color:colors},
        marker:{ size:[14,14,16,16,18], color:colors, symbol:['circle','x','star','diamond','star'],
          line:{color:'#fff',width:1.5} },
        hovertemplate:'<b>%{text}</b><extra></extra>' },
    ];
  })() : null;

  /* ── Split strategy donut ── */
  const splitChart = es.listing_sell_pct != null ? [{
    type:'pie',
    labels:['Sell on Listing Day', 'Hold for Long Term'],
    values:[es.listing_sell_pct, es.hold_pct],
    marker:{ colors:['#00ff88','#a855f7'], line:{color:'#111827',width:3} },
    hole:0.55, textinfo:'label+percent',
    textfont:{color:'#f0f6fc', size:11},
    hovertemplate:'<b>%{label}</b><br>%{value}%<extra></extra>',
  }] : null;

  /* ── Financial KPI bar ── */
  const kpiChart = (es.roe || es.pat_margin || es.ebitda_margin) ? [{
    type:'bar', orientation:'h',
    x:[es.roe||0, es.pat_margin||0, es.ebitda_margin||0, es.fin_score||0],
    y:['ROE %','PAT Margin','EBITDA Margin','Financial Score'],
    marker:{ color:['#00d4ff','#00ff88','#ffa502','#a855f7'],
      line:{color:['#00d4ff','#00ff88','#ffa502','#a855f7'],width:1} },
    text:[(es.roe||0)+'%',(es.pat_margin||0)+'%',(es.ebitda_margin||0)+'%',(es.fin_score||0)+'/100'],
    textposition:'outside',
    hovertemplate:'<b>%{y}</b>: %{x}<extra></extra>',
  }] : null;

  /* ── Financials history chart ── */
  const finChart = d.financials?.length > 1 ? (() => {
    const rows = d.financials.filter(r => r[0] !== 'Period Ended' && r[0] !== 'Particular');
    const labels = rows.map(r => r[0]);
    const revenue = rows.map(r => parseFloat((r[1]||'0').replace(/[Rs.,]/g,'')) || 0);
    const pat     = rows.map(r => parseFloat((r[3]||'0').replace(/[Rs.,]/g,'')) || 0);
    return [
      { type:'bar', name:'Revenue (Cr)', x:labels, y:revenue, marker:{color:'rgba(0,212,255,0.7)'},
        hovertemplate:'%{x}<br>Revenue: Rs.%{y}Cr<extra></extra>' },
      { type:'bar', name:'PAT (Cr)', x:labels, y:pat, marker:{color:'rgba(0,255,136,0.7)'},
        hovertemplate:'%{x}<br>PAT: Rs.%{y}Cr<extra></extra>' },
    ];
  })() : null;

  /* ── Radar chart ── */
  const radarData = [{
    type:'scatterpolar', fill:'toself',
    r:[Math.min(100,es.roe||0), Math.min(100,es.pat_margin||0),
       Math.min(100,es.ebitda_margin||0), es.fin_score||0,
       d.category?.toUpperCase().includes('MAIN') ? 80 : 50],
    theta:['ROE %','PAT Margin','EBITDA Margin','Fin Score','Category'],
    line:{color:rc}, fillcolor:rc+'20', name:d.name?.slice(0,20),
  }];

  return (
    <div style={{ position:'fixed', inset:0, background:'rgba(0,0,0,0.88)',
      zIndex:1000, display:'flex', alignItems:'flex-start', justifyContent:'center',
      padding:'1.5rem', overflowY:'auto' }}
      onClick={e => e.target === e.currentTarget && onClose()}>
      <div style={{ background:'#0d1117', border:'1px solid '+color,
        borderRadius:16, width:'100%', maxWidth:960, padding:'1.75rem', position:'relative' }}>

        {/* Close */}
        <button onClick={onClose} style={{ position:'absolute', top:16, right:16,
          background:'#1c2128', border:'1px solid #30363d', borderRadius:8,
          color:'#8b949e', cursor:'pointer', padding:'4px 12px', fontSize:'0.82rem' }}>
          X Close
        </button>

        {/* Header */}
        <div style={{ display:'flex', gap:16, alignItems:'flex-start', marginBottom:'1.25rem', paddingRight:80 }}>
          <ScoreRing score={d.score||50} size={80}/>
          <div style={{ flex:1 }}>
            <div style={{ fontWeight:900, fontSize:'1.2rem', marginBottom:6 }}>{d.name}</div>
            <div style={{ display:'flex', gap:8, flexWrap:'wrap', marginBottom:8 }}>
              <StatusPill status={d.status}/>
              <span style={{ background:'rgba(168,85,247,0.12)', color:'#a855f7',
                border:'1px solid rgba(168,85,247,0.25)', borderRadius:20,
                padding:'3px 10px', fontSize:'0.68rem', fontWeight:600 }}>{d.category}</span>
              <RecBadge rec={d.recommendation}/>
            </div>
            <div style={{ display:'flex', gap:20, flexWrap:'wrap', fontSize:'0.8rem' }}>
              {[
                {label:'Issue Price', val: ip > 0 ? 'Rs.'+ip.toLocaleString('en-IN') : (d.price_band_full||d.price_band||'TBA')},
                {label:'Issue Size',  val: d.issue_size_full||d.issue_size||'N/A'},
                {label:'Min Invest',  val: d.min_investment||'N/A'},
                {label:'Listing',     val: d.listing_date||'N/A'},
              ].map(f => (
                <div key={f.label}>
                  <div style={{ fontSize:'0.62rem', color:'#8b949e', textTransform:'uppercase', letterSpacing:'0.04em' }}>{f.label}</div>
                  <div style={{ fontWeight:700, color:'#00d4ff' }}>{f.val}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {!detail && (
          <div style={{ display:'flex', alignItems:'center', gap:8, padding:'1rem',
            color:'#8b949e', fontSize:'0.82rem' }}>
            <div className="spinner-sm"/>
            Fetching live data and computing exit strategy...
          </div>
        )}

        {detail && (
          <>
            {/* Tabs */}
            <div style={{ display:'flex', gap:2, background:'#161b22', borderRadius:8,
              padding:4, marginBottom:'1.25rem', overflowX:'auto' }}>
              {[['exit','🎯 Exit Strategy'],['financials','📊 Financials'],
                ['peers','🏭 Peers'],['ai','🤖 AI Analysis']].map(([id,label]) => (
                <button key={id} onClick={() => setTab(id)}
                  style={{ padding:'7px 14px', borderRadius:6, border:'none', cursor:'pointer',
                    fontSize:'0.8rem', fontWeight:500, fontFamily:'inherit', whiteSpace:'nowrap',
                    background: tab===id ? '#1c2128' : 'none',
                    color: tab===id ? '#00d4ff' : '#8b949e',
                    boxShadow: tab===id ? '0 1px 4px rgba(0,0,0,0.3)' : 'none' }}>
                  {label}
                </button>
              ))}
            </div>
            {/* EXIT STRATEGY TAB */}
            {tab === 'exit' && (
              <div>
                {/* Exit level cards */}
                <div style={{ fontWeight:700, color:'#00d4ff', marginBottom:'0.75rem', fontSize:'0.9rem' }}>
                  🎯 Stock-Specific Exit Levels (computed from real financial data)
                </div>
                <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:8, marginBottom:'1.25rem' }}>
                  <ExitCard label="Issue Price"    price={ip}                      pct={0}                         color="#00d4ff" icon="💰" sub="Entry point"/>
                  <ExitCard label="Stop Loss"      price={es.stop_loss_price||0}   pct={es.stop_loss_pct||0}       color="#ff4757" icon="🛑" sub="Exit if falls here"/>
                  <ExitCard label="Listing Target" price={es.listing_target_price||0} pct={es.listing_target_pct||0} color="#00ff88" icon="🚀" sub="Day 1 target"/>
                  <ExitCard label="30-Day Target"  price={es.target_30d_price||0}  pct={es.target_30d_pct||0}      color="#ffa502" icon="📅" sub="1 month hold"/>
                  <ExitCard label="90-Day Target"  price={es.target_90d_price||0}  pct={es.target_90d_pct||0}      color="#a855f7" icon="🏆" sub="3 month hold"/>
                </div>

                {/* Timeline + Split charts */}
                <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1rem', marginBottom:'1rem' }}>
                  <div style={{ background:'#111827', border:'1px solid #21262d', borderRadius:12, padding:'0.75rem' }}>
                    {timelineChart ? (
                      <PlotlyChart data={timelineChart}
                        layout={{ title:'Price Target Timeline', height:300,
                          xaxis:{title:'Days after listing', tickvals:[0,1,30,90], ticktext:['Issue','Listing','30D','90D']},
                          yaxis:{title:'Price (Rs.)', tickprefix:'Rs.'},
                          showlegend:false,
                          shapes:[
                            {type:'line',x0:-2,x1:95,y0:ip,y1:ip,line:{color:'rgba(0,212,255,0.3)',dash:'dot',width:1}},
                            {type:'line',x0:-2,x1:95,y0:es.stop_loss_price||0,y1:es.stop_loss_price||0,
                              line:{color:'rgba(255,71,87,0.4)',dash:'dot',width:1}},
                          ] }}/>
                    ) : (
                      <div style={{ color:'#8b949e', padding:'2rem', textAlign:'center', fontSize:'0.82rem' }}>
                        Issue price TBA — exit levels will appear once price band is announced
                      </div>
                    )}
                  </div>
                  <div style={{ background:'#111827', border:'1px solid #21262d', borderRadius:12, padding:'0.75rem' }}>
                    {splitChart ? (
                      <>
                        <PlotlyChart data={splitChart}
                          layout={{ title:'Recommended Sell Split', height:260, showlegend:true,
                            annotations:[{text:'<b>'+es.listing_sell_pct+'%</b><br>sell day 1',
                              x:0.5,y:0.5,showarrow:false,font:{color:'#f0f6fc',size:12}}] }}/>
                        <div style={{ fontSize:'0.72rem', color:'#8b949e', textAlign:'center', marginTop:4 }}>
                          {es.split_rationale}
                        </div>
                      </>
                    ) : (
                      <div style={{ color:'#8b949e', padding:'2rem', textAlign:'center' }}>Split data unavailable</div>
                    )}
                  </div>
                </div>

                {/* KPI bar + Radar */}
                <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1rem', marginBottom:'1rem' }}>
                  <div style={{ background:'#111827', border:'1px solid #21262d', borderRadius:12, padding:'0.75rem' }}>
                    {kpiChart ? (
                      <PlotlyChart data={kpiChart}
                        layout={{ title:'Financial KPIs (basis for exit levels)', height:280,
                          xaxis:{title:'Value'}, margin:{l:110,r:60,t:40,b:30} }}/>
                    ) : (
                      <div style={{ color:'#8b949e', padding:'2rem', textAlign:'center' }}>KPI data unavailable</div>
                    )}
                  </div>
                  <div style={{ background:'#111827', border:'1px solid #21262d', borderRadius:12, padding:'0.75rem' }}>
                    <PlotlyChart data={radarData}
                      layout={{ title:'IPO Quality Radar', height:280,
                        polar:{radialaxis:{range:[0,100],visible:true}},
                        margin:{l:20,r:20,t:40,b:20} }}/>
                  </div>
                </div>

                {/* Execution guide */}
                <div style={{ background:'linear-gradient(135deg,rgba(0,212,255,0.06),rgba(168,85,247,0.04))',
                  border:'1px solid rgba(0,212,255,0.2)', borderRadius:12, padding:'1rem' }}>
                  <div style={{ fontWeight:700, color:'#00d4ff', marginBottom:'0.75rem', fontSize:'0.9rem' }}>
                    📋 Step-by-Step Execution Guide
                  </div>
                  <div style={{ display:'flex', flexDirection:'column', gap:8 }}>
                    {[
                      { step:'Day 0 — Apply?', action: d.recommendation==='APPLY' ? 'YES — Apply at upper price band' : d.recommendation==='AVOID' ? 'NO — Skip this IPO' : 'OPTIONAL — Apply only if risk appetite is high',
                        color: d.recommendation==='APPLY'?'#00ff88':d.recommendation==='AVOID'?'#ff4757':'#ffa502', icon:'��' },
                      { step:'Listing Day', action: ip > 0 ? 'Sell '+es.listing_sell_pct+'% if price reaches Rs.'+es.listing_target_price+' (+'+es.listing_target_pct+'%). Set stop loss at Rs.'+es.stop_loss_price+' ('+es.stop_loss_pct+'%)' : 'Monitor listing price vs issue price. Sell '+es.listing_sell_pct+'% if listing gain > 10%',
                        color:'#00ff88', icon:'🚀' },
                      { step:'After 30 Days', action: ip > 0 ? 'Review at Rs.'+es.target_30d_price+'. If below issue price, exit remaining. If above target, hold for 90-day target.' : 'Review performance. Exit if below issue price.',
                        color:'#ffa502', icon:'📅' },
                      { step:'After 90 Days', action: ip > 0 ? 'Final exit at Rs.'+es.target_90d_price+' (+'+es.target_90d_pct+'%). Re-evaluate only if fundamentals have improved significantly.' : 'Final review. Exit based on business performance.',
                        color:'#a855f7', icon:'🏆' },
                      { step:'Best For', action: es.investor_type || 'N/A', color:'#00d4ff', icon:'👤' },
                    ].map((s,i) => (
                      <div key={i} style={{ display:'flex', gap:12, alignItems:'flex-start',
                        padding:'8px 10px', background:'rgba(0,0,0,0.2)', borderRadius:8,
                        borderLeft:'3px solid '+s.color }}>
                        <span style={{ fontSize:'1rem', flexShrink:0 }}>{s.icon}</span>
                        <div>
                          <div style={{ fontSize:'0.72rem', color:'#8b949e', textTransform:'uppercase',
                            letterSpacing:'0.04em', marginBottom:2 }}>{s.step}</div>
                          <div style={{ fontSize:'0.82rem', color:'#f0f6fc', fontWeight:500 }}>{s.action}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Valuation vs peers */}
                {es.valuation_vs_peers && es.valuation_vs_peers !== 'N/A' && (
                  <div style={{ marginTop:'0.75rem', padding:'0.75rem 1rem',
                    background:'rgba(0,0,0,0.2)', borderRadius:10,
                    display:'flex', justifyContent:'space-between', alignItems:'center' }}>
                    <span style={{ fontSize:'0.78rem', color:'#8b949e' }}>Valuation vs Peers</span>
                    <span style={{ fontWeight:700, color: es.valuation_vs_peers.includes('Over')?'#ff4757':es.valuation_vs_peers.includes('Under')?'#00ff88':'#ffa502',
                      fontSize:'0.82rem' }}>{es.valuation_vs_peers}</span>
                  </div>
                )}
              </div>
            )}
            {/* FINANCIALS TAB */}
            {tab === 'financials' && (
              <div>
                <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:8, marginBottom:'1rem' }}>
                  {[
                    {label:'ROE',          val:d.roe||'N/A',          good: v => parseFloat(v)>15},
                    {label:'ROCE',         val:d.roce||'N/A',         good: v => parseFloat(v)>15},
                    {label:'EBITDA Margin',val:d.ebitda_margin||'N/A',good: v => parseFloat(v)>10},
                    {label:'PAT Margin',   val:d.pat_margin||'N/A',   good: v => parseFloat(v)>8},
                    {label:'Debt/Equity',  val:d.debt_equity||'N/A',  good: v => parseFloat(v)<1},
                  ].map(f => {
                    const isGood = f.val!=='N/A' ? f.good(f.val) : null;
                    const c = isGood===true?'#00ff88':isGood===false?'#ff4757':'#00d4ff';
                    return (
                      <div key={f.label} style={{ background:'#161b22', borderRadius:10,
                        padding:'0.75rem', textAlign:'center', borderBottom:'2px solid '+c }}>
                        <div style={{ fontSize:'0.62rem', color:'#8b949e', marginBottom:3,
                          textTransform:'uppercase', letterSpacing:'0.04em' }}>{f.label}</div>
                        <div style={{ fontWeight:800, color:c, fontSize:'1rem' }}>{f.val}</div>
                      </div>
                    );
                  })}
                </div>
                {finChart && (
                  <div style={{ background:'#111827', border:'1px solid #21262d', borderRadius:12, padding:'0.75rem', marginBottom:'1rem' }}>
                    <PlotlyChart data={finChart}
                      layout={{ title:'Revenue & PAT History (Rs. Cr)', height:300,
                        barmode:'group', yaxis:{title:'Rs. Crores'} }}/>
                  </div>
                )}
                {es.revenue_growth > 0 && (
                  <div style={{ padding:'0.75rem 1rem', background:'rgba(0,255,136,0.06)',
                    border:'1px solid rgba(0,255,136,0.2)', borderRadius:10, fontSize:'0.82rem' }}>
                    Revenue CAGR: <strong style={{ color:'#00ff88' }}>{es.revenue_growth}%</strong> per year
                    {es.revenue_growth > 20 ? ' — Strong growth' : es.revenue_growth > 10 ? ' — Moderate growth' : ' — Slow growth'}
                  </div>
                )}
                {d.promoter_pre && d.promoter_pre !== 'N/A' && (
                  <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:8, marginTop:'0.75rem' }}>
                    {[{label:'Pre-Issue Promoter',val:d.promoter_pre,color:'#00d4ff'},
                      {label:'Post-Issue Promoter',val:d.promoter_post||'N/A',color:'#00ff88'}].map(f => (
                      <div key={f.label} style={{ background:'#161b22', borderRadius:10,
                        padding:'0.75rem', textAlign:'center' }}>
                        <div style={{ fontSize:'0.68rem', color:'#8b949e', marginBottom:4 }}>{f.label}</div>
                        <div style={{ fontWeight:900, color:f.color, fontSize:'1.3rem' }}>{f.val}</div>
                      </div>
                    ))}
                  </div>
                )}
                {d.objects_of_issue?.length > 0 && (
                  <div style={{ marginTop:'0.75rem' }}>
                    <div style={{ fontWeight:600, color:'#00d4ff', marginBottom:'0.5rem', fontSize:'0.85rem' }}>
                      Use of IPO Proceeds
                    </div>
                    {d.objects_of_issue.map((o,i) => (
                      <div key={i} style={{ display:'flex', justifyContent:'space-between',
                        padding:'7px 10px', background:'#161b22', borderRadius:7, marginBottom:4, fontSize:'0.8rem' }}>
                        <span style={{ color:'#8b949e' }}>{o.purpose}</span>
                        <span style={{ fontWeight:600, color:'#00d4ff' }}>{o.amount}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* PEERS TAB */}
            {tab === 'peers' && (
              <div>
                {d.peers?.length > 0 ? (
                  <>
                    <div style={{ overflowX:'auto', borderRadius:10, border:'1px solid #21262d', marginBottom:'1rem' }}>
                      <table style={{ width:'100%', borderCollapse:'collapse', fontSize:'0.82rem' }}>
                        <thead>
                          <tr>
                            {['Company','EPS','P/E Ratio','RoNW %','NAV','Revenue'].map(h => (
                              <th key={h} style={{ background:'#161b22', color:'#00d4ff', padding:'10px 12px',
                                textAlign:'left', fontWeight:600, fontSize:'0.72rem',
                                textTransform:'uppercase', letterSpacing:'0.04em',
                                borderBottom:'1px solid #21262d' }}>{h}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {d.peers.map((p,i) => (
                            <tr key={i} style={{ borderBottom:'1px solid #21262d' }}>
                              <td style={{ padding:'10px 12px', fontWeight:600 }}>{p.company}</td>
                              <td style={{ padding:'10px 12px', color:'#00d4ff' }}>{p.eps}</td>
                              <td style={{ padding:'10px 12px', color:'#ffa502' }}>{p.pe}</td>
                              <td style={{ padding:'10px 12px', color:'#00ff88' }}>{p.ronw}</td>
                              <td style={{ padding:'10px 12px' }}>{p.nav}</td>
                              <td style={{ padding:'10px 12px', color:'#8b949e' }}>{p.income}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                    {es.peer_avg_pe > 0 && (
                      <div style={{ padding:'0.75rem 1rem', background:'rgba(0,0,0,0.2)',
                        borderRadius:10, fontSize:'0.82rem',
                        display:'flex', justifyContent:'space-between' }}>
                        <span style={{ color:'#8b949e' }}>Peer Average P/E</span>
                        <span style={{ fontWeight:700, color:'#ffa502' }}>{es.peer_avg_pe}x</span>
                      </div>
                    )}
                    {es.valuation_vs_peers && es.valuation_vs_peers !== 'N/A' && (
                      <div style={{ padding:'0.75rem 1rem', background:'rgba(0,0,0,0.2)',
                        borderRadius:10, fontSize:'0.82rem', marginTop:6,
                        display:'flex', justifyContent:'space-between' }}>
                        <span style={{ color:'#8b949e' }}>Valuation Assessment</span>
                        <span style={{ fontWeight:700,
                          color: es.valuation_vs_peers.includes('Over')?'#ff4757':es.valuation_vs_peers.includes('Under')?'#00ff88':'#ffa502' }}>
                          {es.valuation_vs_peers}
                        </span>
                      </div>
                    )}
                  </>
                ) : (
                  <div style={{ color:'#8b949e', padding:'2rem', textAlign:'center' }}>
                    Peer comparison data not available for this IPO.
                  </div>
                )}
              </div>
            )}

            {/* AI ANALYSIS TAB */}
            {tab === 'ai' && (
              <div>
                {d.ai_analysis ? (
                  <div style={{ background:'linear-gradient(135deg,rgba(168,85,247,0.08),rgba(0,212,255,0.03))',
                    border:'1px solid rgba(168,85,247,0.3)', borderRadius:12, padding:'1.25rem' }}>
                    <div style={{ fontWeight:700, color:'#a855f7', marginBottom:'0.75rem',
                      display:'flex', alignItems:'center', gap:8, fontSize:'0.95rem' }}>
                      AI Analysis — Groq Llama 3.3 70B
                      <span style={{ background:'rgba(168,85,247,0.12)', color:'#a855f7',
                        border:'1px solid rgba(168,85,247,0.25)', borderRadius:20,
                        padding:'2px 8px', fontSize:'0.65rem', fontWeight:600 }}>Live Analysis</span>
                    </div>
                    <div style={{ color:'#f0f6fc', lineHeight:1.85, fontSize:'0.875rem', whiteSpace:'pre-wrap' }}>
                      {d.ai_analysis}
                    </div>
                  </div>
                ) : (
                  <div style={{ padding:'1rem', background:'rgba(0,212,255,0.06)',
                    border:'1px solid rgba(0,212,255,0.2)', borderRadius:10,
                    fontSize:'0.82rem', color:'#8b949e' }}>
                    AI analysis requires GROQ_API_KEY in .env file.
                  </div>
                )}
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
  const [data,     setData]     = useState(null);
  const [loading,  setLoading]  = useState(true);
  const [filter,   setFilter]   = useState('All');
  const [view,     setView]     = useState('cards');
  const [selected, setSelected] = useState(null);
  const [sortBy,   setSortBy]   = useState('status');

  const load = useCallback(() => {
    setLoading(true);
    ipo.live()
      .then(r => setData(r.data))
      .catch(() => toast.error('Failed to fetch IPO data'))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const ipos = data?.ipos || [];
  const order = { Open:0, Upcoming:1, Closed:2, Unknown:3 };
  const sorted = [...ipos].sort((a,b) => {
    if (sortBy==='score') return b.score - a.score;
    if (sortBy==='size')  return (parseFloat(b.issue_size)||0) - (parseFloat(a.issue_size)||0);
    return (order[a.status]||3) - (order[b.status]||3);
  });
  const filtered = filter==='All' ? sorted : sorted.filter(i => i.status===filter);

  const scoreBar = ipos.slice(0,15).length ? [{
    type:'bar',
    x: ipos.slice(0,15).map(i => (i.name||'').slice(0,16)+((i.name||'').length>16?'...':'')),
    y: ipos.slice(0,15).map(i => i.score),
    marker:{ color: ipos.slice(0,15).map(i => i.score>=65?'rgba(0,255,136,0.8)':i.score>=45?'rgba(255,165,2,0.8)':'rgba(255,71,87,0.8)') },
    text: ipos.slice(0,15).map(i => i.score+'/100'),
    textposition:'outside', textfont:{size:10},
    hovertemplate:'<b>%{x}</b><br>Score: %{y}/100<extra></extra>',
  }] : [];

  const statusPie = ipos.length ? [{
    type:'pie',
    labels:['Open','Upcoming','Closed','Unknown'],
    values:[ipos.filter(i=>i.status==='Open').length, ipos.filter(i=>i.status==='Upcoming').length,
            ipos.filter(i=>i.status==='Closed').length, ipos.filter(i=>i.status==='Unknown').length],
    marker:{ colors:['#00ff88','#00d4ff','#8b949e','#ffa502'], line:{color:'#060910',width:2} },
    hole:0.5, textinfo:'label+value', textfont:{color:'#f0f6fc',size:11},
    hovertemplate:'<b>%{label}</b><br>%{value} IPOs<extra></extra>',
  }] : [];

  const recPie = ipos.length ? [{
    type:'pie',
    labels:['APPLY','NEUTRAL','AVOID'],
    values:[ipos.filter(i=>i.recommendation==='APPLY').length,
            ipos.filter(i=>i.recommendation==='NEUTRAL').length,
            ipos.filter(i=>i.recommendation==='AVOID').length],
    marker:{ colors:['#00ff88','#ffa502','#ff4757'], line:{color:'#060910',width:2} },
    hole:0.5, textinfo:'label+value', textfont:{color:'#f0f6fc',size:11},
    hovertemplate:'<b>%{label}</b><br>%{value} IPOs<extra></extra>',
  }] : [];

  return (
    <div>
      <div style={{ marginBottom:'1.75rem', paddingBottom:'1rem', borderBottom:'1px solid #21262d' }}>
        <div style={{ fontSize:'1.6rem', fontWeight:800,
          background:'linear-gradient(135deg,#00d4ff,#00ff88)',
          WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent',
          backgroundClip:'text', marginBottom:'0.25rem' }}>
          IPO Intelligence Hub
        </div>
        <div style={{ fontSize:'0.8rem', color:'#8b949e', display:'flex', alignItems:'center', gap:8 }}>
          <span style={{ width:8, height:8, borderRadius:'50%', background:'#00ff88',
            animation:'pulse 2s infinite', display:'inline-block' }}/>
          Live data from ipowatch.in · Stock-specific exit strategy · AI analysis per IPO · Click any card
          <button style={{ marginLeft:'auto', background:'#1c2128', border:'1px solid #30363d',
            borderRadius:8, color:'#8b949e', cursor:'pointer', padding:'5px 12px', fontSize:'0.75rem',
            fontFamily:'inherit' }} onClick={load}>Refresh</button>
        </div>
      </div>

      {loading && (
        <div style={{ display:'flex', alignItems:'center', justifyContent:'center',
          gap:12, color:'#8b949e', padding:'4rem 2rem', flexDirection:'column' }}>
          <div style={{ width:32, height:32, border:'3px solid #21262d',
            borderTopColor:'#00d4ff', borderRadius:'50%', animation:'spin 0.7s linear infinite' }}/>
          <div style={{ fontSize:'0.875rem' }}>Fetching live IPO data from ipowatch.in...</div>
        </div>
      )}

      {!loading && data && (
        <>
          <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:'1rem', marginBottom:'1.25rem' }}>
            {[
              {label:'Total IPOs',  val:data.total,          color:'#00d4ff'},
              {label:'Open Now',    val:data.open_count,     color:'#00ff88'},
              {label:'Upcoming',    val:data.upcoming_count, color:'#00d4ff'},
              {label:'Closed',      val:data.closed_count,   color:'#8b949e'},
              {label:'APPLY Rated', val:ipos.filter(i=>i.recommendation==='APPLY').length, color:'#00ff88'},
            ].map(k => (
              <div key={k.label} style={{ background:'#111827', border:'1px solid #21262d',
                borderRadius:14, padding:'1.2rem 1.4rem', borderLeft:'3px solid '+k.color }}>
                <div style={{ fontSize:'0.72rem', color:'#8b949e', textTransform:'uppercase',
                  letterSpacing:'0.05em', marginBottom:6 }}>{k.label}</div>
                <div style={{ fontSize:'2rem', fontWeight:800, color:k.color }}>{k.val}</div>
              </div>
            ))}
          </div>

          <div style={{ display:'flex', gap:8, marginBottom:'1.25rem', flexWrap:'wrap', alignItems:'center' }}>
            {['All','Open','Upcoming','Closed'].map(f => (
              <button key={f} onClick={() => setFilter(f)}
                style={{ padding:'6px 14px', borderRadius:8, border:'none', cursor:'pointer',
                  fontSize:'0.8rem', fontWeight:600, fontFamily:'inherit',
                  background: filter===f ? 'linear-gradient(135deg,#00d4ff,#0099cc)' : '#1c2128',
                  color: filter===f ? '#000' : '#8b949e',
                  boxShadow: filter===f ? '0 2px 12px rgba(0,212,255,0.3)' : 'none' }}>
                {f==='Open'?'🟢':f==='Upcoming'?'🔵':f==='Closed'?'⚫':'📋'} {f}
                {' '}({f==='All'?ipos.length:ipos.filter(i=>i.status===f).length})
              </button>
            ))}
            <div style={{ marginLeft:8, display:'flex', alignItems:'center', gap:6 }}>
              <span style={{ fontSize:'0.75rem', color:'#8b949e' }}>Sort:</span>
              {[['status','Status'],['score','Score'],['size','Size']].map(([id,label]) => (
                <button key={id} onClick={() => setSortBy(id)}
                  style={{ padding:'5px 10px', borderRadius:8, border:'none', cursor:'pointer',
                    fontSize:'0.75rem', fontFamily:'inherit',
                    background: sortBy===id ? 'linear-gradient(135deg,#00d4ff,#0099cc)' : '#1c2128',
                    color: sortBy===id ? '#000' : '#8b949e' }}>{label}</button>
              ))}
            </div>
            <div style={{ marginLeft:'auto', display:'flex', gap:4 }}>
              {[['cards','Cards'],['analytics','Analytics']].map(([id,label]) => (
                <button key={id} onClick={() => setView(id)}
                  style={{ padding:'6px 12px', borderRadius:8, border:'none', cursor:'pointer',
                    fontSize:'0.78rem', fontFamily:'inherit',
                    background: view===id ? 'linear-gradient(135deg,#00d4ff,#0099cc)' : '#1c2128',
                    color: view===id ? '#000' : '#8b949e' }}>{label}</button>
              ))}
            </div>
          </div>

          {view === 'cards' && (
            <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:'1rem' }}>
              {filtered.length === 0 && (
                <div style={{ gridColumn:'1/-1', textAlign:'center', color:'#8b949e', padding:'3rem' }}>
                  No IPOs found for this filter.
                </div>
              )}
              {filtered.map((item,i) => {
                const sc = C[item.status]||'#8b949e';
                const rc2 = RC[item.recommendation]||'#ffa502';
                return (
                  <div key={i} onClick={() => setSelected(item)}
                    style={{ background:'#111827', border:'1px solid #21262d',
                      borderTop:'3px solid '+sc, borderRadius:14, padding:'1.25rem',
                      cursor:'pointer', transition:'all 0.2s' }}
                    onMouseEnter={e => { e.currentTarget.style.transform='translateY(-3px)'; e.currentTarget.style.borderColor=sc; }}
                    onMouseLeave={e => { e.currentTarget.style.transform='none'; e.currentTarget.style.borderColor='#21262d'; }}>
                    <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', gap:8, marginBottom:10 }}>
                      <div style={{ flex:1 }}>
                        <div style={{ fontWeight:700, fontSize:'0.9rem', lineHeight:1.3, marginBottom:6 }}>{item.name}</div>
                        <div style={{ display:'flex', gap:6, flexWrap:'wrap' }}>
                          <StatusPill status={item.status}/>
                          <span style={{ background:'rgba(168,85,247,0.12)', color:'#a855f7',
                            border:'1px solid rgba(168,85,247,0.25)', borderRadius:20,
                            padding:'3px 8px', fontSize:'0.65rem', fontWeight:600 }}>{item.category}</span>
                        </div>
                      </div>
                      <ScoreRing score={item.score||50} size={60}/>
                    </div>
                    <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'5px 12px',
                      fontSize:'0.78rem', marginBottom:10 }}>
                      {[{label:'Price Band',val:item.price_band||'TBA'},{label:'Issue Size',val:item.issue_size||'N/A'},
                        {label:'Open Date',val:item.open_date||'N/A'},{label:'Close Date',val:item.close_date||'N/A'}].map(r => (
                        <div key={r.label}>
                          <div style={{ color:'#8b949e', fontSize:'0.62rem', marginBottom:1,
                            textTransform:'uppercase', letterSpacing:'0.04em' }}>{r.label}</div>
                          <div style={{ fontWeight:500 }}>{r.val}</div>
                        </div>
                      ))}
                    </div>
                    <div style={{ marginBottom:10 }}>
                      <div style={{ display:'flex', justifyContent:'space-between', fontSize:'0.68rem', marginBottom:3 }}>
                        <span style={{ color:'#8b949e' }}>IPO Score</span>
                        <span style={{ color:rc2, fontWeight:700 }}>{item.score}/100</span>
                      </div>
                      <div style={{ background:'#21262d', borderRadius:4, height:5 }}>
                        <div style={{ width:item.score+'%', height:'100%',
                          background:'linear-gradient(90deg,'+rc2+','+rc2+'aa)',
                          borderRadius:4, transition:'width 0.6s ease' }}/>
                      </div>
                    </div>
                    <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
                      <RecBadge rec={item.recommendation}/>
                      <span style={{ fontSize:'0.65rem', color:'#484f58' }}>Click for exit strategy</span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {view === 'analytics' && ipos.length > 0 && (
            <div style={{ display:'flex', flexDirection:'column', gap:'1rem' }}>
              <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:'1rem' }}>
                <div style={{ background:'#111827', border:'1px solid #21262d', borderRadius:14, padding:'0.75rem' }}>
                  <PlotlyChart data={statusPie}
                    layout={{ title:'IPO Status Distribution', height:320, showlegend:true,
                      annotations:[{text:'<b>'+ipos.length+'</b><br>total',x:0.5,y:0.5,showarrow:false,font:{color:'#f0f6fc',size:13}}] }}/>
                </div>
                <div style={{ background:'#111827', border:'1px solid #21262d', borderRadius:14, padding:'0.75rem' }}>
                  <PlotlyChart data={recPie}
                    layout={{ title:'Recommendation Distribution', height:320, showlegend:true,
                      annotations:[{text:'<b>AI</b><br>Recs',x:0.5,y:0.5,showarrow:false,font:{color:'#f0f6fc',size:13}}] }}/>
                </div>
                <div style={{ background:'#111827', border:'1px solid #21262d', borderRadius:14, padding:'0.75rem' }}>
                  <PlotlyChart data={[{type:'bar',x:['APPLY','NEUTRAL','AVOID'],
                    y:[ipos.filter(i=>i.recommendation==='APPLY').length,
                       ipos.filter(i=>i.recommendation==='NEUTRAL').length,
                       ipos.filter(i=>i.recommendation==='AVOID').length],
                    marker:{color:['rgba(0,255,136,0.75)','rgba(255,165,2,0.75)','rgba(255,71,87,0.75)']},
                    text:[ipos.filter(i=>i.recommendation==='APPLY').length+' IPOs',
                          ipos.filter(i=>i.recommendation==='NEUTRAL').length+' IPOs',
                          ipos.filter(i=>i.recommendation==='AVOID').length+' IPOs'],
                    textposition:'outside',
                    hovertemplate:'<b>%{x}</b><br>%{y} IPOs<extra></extra>'}]}
                    layout={{ title:'Recommendation Breakdown', height:320, yaxis:{title:'Count'}, bargap:0.4 }}/>
                </div>
              </div>
              <div style={{ background:'#111827', border:'1px solid #21262d', borderRadius:14, padding:'0.75rem' }}>
                <PlotlyChart data={scoreBar}
                  layout={{ title:'IPO Scores — Top 15 (Green=APPLY, Orange=NEUTRAL, Red=AVOID)',
                    height:420, yaxis:{title:'Score /100',range:[0,115]}, xaxis:{tickangle:-30},
                    shapes:[
                      {type:'line',x0:-0.5,x1:14.5,y0:65,y1:65,line:{color:'rgba(0,255,136,0.4)',dash:'dot',width:2}},
                      {type:'line',x0:-0.5,x1:14.5,y0:45,y1:45,line:{color:'rgba(255,71,87,0.4)',dash:'dot',width:2}},
                    ],
                    annotations:[
                      {x:14.5,y:65,text:'APPLY',showarrow:false,font:{color:'#00ff88',size:10},xanchor:'right'},
                      {x:14.5,y:45,text:'AVOID',showarrow:false,font:{color:'#ff4757',size:10},xanchor:'right'},
                    ] }}/>
              </div>
            </div>
          )}

          <div style={{ marginTop:'1rem', fontSize:'0.7rem', color:'#484f58', textAlign:'center' }}>
            Data: ipowatch.in (live) · Exit levels computed from real financial data (ROE, margins, growth, peers)
            · Last fetched: {new Date(data.timestamp).toLocaleTimeString('en-IN')}
          </div>
        </>
      )}

      {selected && <IPODetailModal ipoItem={selected} onClose={() => setSelected(null)}/>}
    </div>
  );
}
