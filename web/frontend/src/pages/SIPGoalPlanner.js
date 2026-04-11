import React, { useState, useEffect } from 'react';
import { sip } from '../api';
import PlotlyChart from '../components/PlotlyChart';
import toast from 'react-hot-toast';

/* ── Constants ── */
const GOAL_TYPES = [
  { id: "Child's Education",  icon: '🎓', desc: 'School, college, MBA abroad',    amount: 2500000, years: 15 },
  { id: 'Home Down Payment',  icon: '🏠', desc: 'Buy your dream home',            amount: 2000000, years: 7  },
  { id: 'Retirement Corpus',  icon: '👴', desc: 'Retire comfortably',             amount: 10000000,years: 25 },
  { id: 'Wedding',            icon: '💍', desc: 'Your or child\'s wedding',       amount: 1500000, years: 5  },
  { id: 'Dream Vacation',     icon: '✈️', desc: 'International travel',           amount: 500000,  years: 3  },
  { id: 'Car Purchase',       icon: '🚗', desc: 'Buy a new car',                  amount: 800000,  years: 4  },
  { id: 'Emergency Fund',     icon: '🏥', desc: '6 months of expenses',           amount: 600000,  years: 2  },
  { id: 'Custom Goal',        icon: '🎯', desc: 'Define your own goal',           amount: 1000000, years: 10 },
];

const PC = { Conservative: '#00d4ff', Moderate: '#00ff88', Aggressive: '#ff9800' };
const PI = { Conservative: '🛡️', Moderate: '⚖️', Aggressive: '🚀' };
const PDESC = {
  Conservative: 'Debt & Gilt funds · Low risk · Stable 7-9% returns',
  Moderate:     'Large Cap & Index funds · Medium risk · 11-14% returns',
  Aggressive:   'Small & Mid Cap funds · High risk · 15-20% returns',
};

/* ── Goal Type Selector Card ── */
function GoalCard({ goal, selected, onClick }) {
  const active = selected === goal.id;
  return (
    <div onClick={onClick} style={{
      background: active
        ? 'linear-gradient(135deg,rgba(0,212,255,0.15),rgba(0,255,136,0.08))'
        : 'var(--bg-card)',
      border: `1px solid ${active ? 'var(--accent)' : 'var(--border)'}`,
      borderRadius: 12, padding: '0.9rem 1rem',
      cursor: 'pointer', transition: 'all 0.2s',
      transform: active ? 'translateY(-2px)' : 'none',
      boxShadow: active ? '0 4px 20px rgba(0,212,255,0.2)' : 'none',
    }}>
      <div style={{ fontSize: '1.5rem', marginBottom: 4 }}>{goal.icon}</div>
      <div style={{ fontWeight: 700, fontSize: '0.85rem',
        color: active ? 'var(--accent)' : 'var(--text-primary)' }}>{goal.id}</div>
      <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginTop: 2 }}>{goal.desc}</div>
    </div>
  );
}

/* ── Profile Card ── */
function ProfileCard({ profile, data, selected, onClick }) {
  const color = PC[profile];
  const active = selected === profile;
  return (
    <div onClick={onClick} style={{
      background: active ? `${color}12` : 'var(--bg-card)',
      border: `2px solid ${active ? color : 'var(--border)'}`,
      borderRadius: 14, padding: '1.25rem',
      cursor: 'pointer', transition: 'all 0.2s', textAlign: 'center',
      transform: active ? 'translateY(-3px)' : 'none',
      boxShadow: active ? `0 6px 24px ${color}30` : 'none',
    }}>
      <div style={{ fontSize: '1.6rem', marginBottom: 4 }}>{PI[profile]}</div>
      <div style={{ fontWeight: 800, color, fontSize: '1rem', marginBottom: 2 }}>{profile}</div>
      <div style={{ fontSize: '0.68rem', color: 'var(--text-secondary)', marginBottom: 10 }}>
        {PDESC[profile]}
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--text-primary)', lineHeight: 1 }}>
        ₹{data?.monthly_sip?.toLocaleString('en-IN')}
      </div>
      <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', marginTop: 2 }}>/month</div>
      <div style={{ marginTop: 8, padding: '4px 0',
        borderTop: `1px solid ${color}33`, fontSize: '0.75rem' }}>
        <span style={{ color }}>{data?.return_pct}% p.a.</span>
        <span style={{ color: 'var(--text-secondary)', marginLeft: 6 }}>
          Corpus: ₹{((data?.total_value || 0) / 1e5).toFixed(1)}L
        </span>
      </div>
    </div>
  );
}

/* ── Fund Card ── */
function FundCard({ fund, rank }) {
  const colors = ['#ffd700', '#c0c0c0', '#cd7f32', '#00d4ff', '#00ff88'];
  return (
    <div style={{
      background: 'var(--bg-secondary)', borderRadius: 10,
      padding: '0.85rem 1rem', border: '1px solid var(--border)',
      display: 'flex', alignItems: 'center', gap: 12,
    }}>
      <div style={{ width: 28, height: 28, borderRadius: '50%',
        background: `${colors[rank] || '#00d4ff'}22`,
        border: `2px solid ${colors[rank] || '#00d4ff'}`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '0.75rem', fontWeight: 800, color: colors[rank] || '#00d4ff',
        flexShrink: 0 }}>#{rank + 1}</div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontWeight: 600, fontSize: '0.82rem',
          whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {fund.name}
        </div>
        <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginTop: 2 }}>
          NAV: ₹{fund.nav?.toFixed(2)} · {fund.nav_date}
        </div>
      </div>
      {fund.cagr_3y && (
        <div style={{ textAlign: 'right', flexShrink: 0 }}>
          <div style={{ fontWeight: 800, color: '#00ff88', fontSize: '0.9rem' }}>
            {fund.cagr_3y}%
          </div>
          <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)' }}>3Y CAGR</div>
        </div>
      )}
    </div>
  );
}

/* ── Main Component ── */
export default function SIPGoalPlanner() {
  const [tab,         setTab]         = useState('plan');
  const [goalType,    setGoalType]    = useState("Child's Education");
  const [goalName,    setGoalName]    = useState("Child's Education");
  const [target,      setTarget]      = useState(2500000);
  const [years,       setYears]       = useState(15);
  const [inflation,   setInflation]   = useState(6);
  const [existing,    setExisting]    = useState(0);
  const [result,      setResult]      = useState(null);
  const [loading,     setLoading]     = useState(false);
  const [selProfile,  setSelProfile]  = useState('Moderate');
  const [goals,       setGoals]       = useState([]);
  const [saveProfile, setSaveProfile] = useState('Moderate');

  /* Auto-fill when goal type changes */
  useEffect(() => {
    const g = GOAL_TYPES.find(g => g.id === goalType);
    if (g) { setTarget(g.amount); setYears(g.years); setGoalName(g.id); }
  }, [goalType]);

  const calculate = async () => {
    setLoading(true); setResult(null);
    try {
      const r = await sip.calculate({
        target_today: target, years, inflation,
        existing_savings: existing, goal_name: goalName, goal_type: goalType,
      });
      setResult(r.data);
      toast.success('Live AMFI data fetched!');
    } catch (e) { toast.error('Calculation failed. Check backend.'); }
    finally { setLoading(false); }
  };

  const loadGoals = () => sip.getGoals().then(r => setGoals(r.data)).catch(() => {});
  useEffect(() => { if (tab === 'goals') loadGoals(); }, [tab]);

  const saveGoal = async () => {
    if (!result) return;
    const p = result.profiles[saveProfile];
    await sip.saveGoal({
      goal_name: goalName, goal_type: goalType,
      target_today: target, years, inflation,
      existing_savings: existing, monthly_sip: p.monthly_sip,
      risk_profile: saveProfile, expected_return: p.return_pct,
    });
    toast.success(`Goal "${goalName}" saved!`);
  };

  const deleteGoal = async (id) => {
    await sip.deleteGoal(id); loadGoals(); toast.success('Goal deleted');
  };

  /* Derived values */
  const fv = target * Math.pow(1 + inflation / 100, years);
  const selData = result?.profiles?.[selProfile];

  /* ── Charts ── */
  const growthChart = result ? [
    {
      type: 'scatter', name: 'Amount Invested',
      x: result.profiles.Moderate.series.map(s => s.year),
      y: result.profiles.Moderate.series.map(s => s.invested),
      line: { color: '#8b949e', dash: 'dot', width: 2 },
      fill: 'tozeroy', fillcolor: 'rgba(139,148,158,0.04)',
      hovertemplate: 'Year %{x}<br>Invested: ₹%{y:,.0f}<extra></extra>',
    },
    ...Object.entries(result.profiles).map(([p, d]) => ({
      type: 'scatter', name: `${p} (${d.return_pct}% p.a.)`,
      x: d.series.map(s => s.year),
      y: d.series.map(s => s.value),
      line: { color: PC[p], width: 2.5 },
      hovertemplate: `${p}<br>Year %{x}<br>Value: ₹%{y:,.0f}<extra></extra>`,
    })),
  ] : [];

  const inflationChart = [
    {
      type: 'scatter', name: 'Inflation-Adjusted Target',
      x: Array.from({ length: years + 1 }, (_, i) => i),
      y: Array.from({ length: years + 1 }, (_, i) =>
        Math.round(target * Math.pow(1 + inflation / 100, i))),
      line: { color: '#ff4757', width: 2.5 },
      fill: 'tozeroy', fillcolor: 'rgba(255,71,87,0.07)',
      hovertemplate: 'Year %{x}<br>Need: ₹%{y:,.0f}<extra></extra>',
    },
    {
      type: 'scatter', name: "Today's Value",
      x: Array.from({ length: years + 1 }, (_, i) => i),
      y: Array.from({ length: years + 1 }, () => target),
      line: { color: '#8b949e', dash: 'dot', width: 1.5 },
      hovertemplate: "Today's value: ₹%{y:,.0f}<extra></extra>",
    },
  ];

  const sipCompareBar = result ? [{
    type: 'bar',
    x: Object.keys(result.profiles),
    y: Object.values(result.profiles).map(p => p.monthly_sip),
    marker: { color: Object.values(PC), line: { color: Object.values(PC), width: 1 } },
    text: Object.values(result.profiles).map(p => `₹${p.monthly_sip.toLocaleString('en-IN')}`),
    textposition: 'outside',
    hovertemplate: '<b>%{x}</b><br>SIP: ₹%{y:,.0f}/mo<extra></extra>',
  }] : [];

  const corpusBar = result ? [
    {
      type: 'bar', name: 'Amount Invested',
      x: Object.keys(result.profiles),
      y: Object.values(result.profiles).map(p => p.total_invested),
      marker: { color: 'rgba(0,212,255,0.7)' },
      hovertemplate: '<b>%{x}</b><br>Invested: ₹%{y:,.0f}<extra></extra>',
    },
    {
      type: 'bar', name: 'Returns Earned',
      x: Object.keys(result.profiles),
      y: Object.values(result.profiles).map(p => p.total_gain),
      marker: { color: 'rgba(0,255,136,0.7)' },
      hovertemplate: '<b>%{x}</b><br>Returns: ₹%{y:,.0f}<extra></extra>',
    },
  ] : [];

  /* Year-by-year gain for selected profile */
  const gainArea = selData?.series?.length ? [{
    type: 'scatter', name: 'Portfolio Value',
    x: selData.series.map(s => s.year),
    y: selData.series.map(s => s.value),
    line: { color: PC[selProfile], width: 2.5 },
    fill: 'tozeroy', fillcolor: `${PC[selProfile]}12`,
    hovertemplate: 'Year %{x}<br>Value: ₹%{y:,.0f}<extra></extra>',
  }, {
    type: 'scatter', name: 'Invested',
    x: selData.series.map(s => s.year),
    y: selData.series.map(s => s.invested),
    line: { color: '#8b949e', dash: 'dot', width: 1.5 },
    hovertemplate: 'Year %{x}<br>Invested: ₹%{y:,.0f}<extra></extra>',
  }] : [];

  return (
    <div>
      {/* ── Header ── */}
      <div className="page-header">
        <div className="section-title">🎯 SIP Goal Planner</div>
        <div className="section-subtitle">
          <span className="pulse-dot" />
          Live AMFI returns · Inflation-adjusted · AI-powered advice · Real fund recommendations
        </div>
      </div>

      {/* ── Tabs ── */}
      <div className="tab-bar">
        {[['plan', '🎯 Plan My SIP'], ['goals', '📋 My Saved Goals']].map(([id, label]) => (
          <button key={id} className={`tab ${tab === id ? 'active' : ''}`}
            onClick={() => setTab(id)}>{label}</button>
        ))}
      </div>

      {/* ══════════════════════════════════════════════════════════
          TAB 1 — PLAN
      ══════════════════════════════════════════════════════════ */}
      {tab === 'plan' && (
        <div>
          {/* STEP 1 — Goal Type */}
          <div className="card" style={{ marginBottom: '1.25rem' }}>
            <div style={{ fontWeight: 700, color: 'var(--accent)', marginBottom: '0.75rem', fontSize: '1rem' }}>
              Step 1 — Why are you starting this SIP?
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 10 }}>
              {GOAL_TYPES.map(g => (
                <GoalCard key={g.id} goal={g} selected={goalType}
                  onClick={() => setGoalType(g.id)} />
              ))}
            </div>
          </div>

          {/* STEP 2 — Parameters */}
          <div className="card" style={{ marginBottom: '1.25rem' }}>
            <div style={{ fontWeight: 700, color: 'var(--accent)', marginBottom: '1rem', fontSize: '1rem' }}>
              Step 2 — Set Your Parameters
            </div>
            <div className="grid-2">
              {/* Left column */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                <div>
                  <label>Goal Name</label>
                  <input value={goalName} onChange={e => setGoalName(e.target.value)}
                    placeholder="e.g. Daughter's MBA Abroad" />
                </div>
                <div>
                  <label>Target Amount in Today's ₹</label>
                  <input type="number" value={target} step={50000}
                    onChange={e => setTarget(Number(e.target.value))} />
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginTop: 3 }}>
                    How much do you need in today's money?
                  </div>
                </div>
                <div>
                  <label>Existing Savings for this Goal (₹)</label>
                  <input type="number" value={existing} step={10000}
                    onChange={e => setExisting(Number(e.target.value))} />
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginTop: 3 }}>
                    Any lump sum already saved? (Enter 0 if none)
                  </div>
                </div>
              </div>

              {/* Right column — sliders */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                    <label style={{ margin: 0 }}>Investment Period</label>
                    <span style={{ fontWeight: 800, color: 'var(--accent)', fontSize: '1.1rem' }}>
                      {years} years
                    </span>
                  </div>
                  <input type="range" min={1} max={40} value={years}
                    onChange={e => setYears(Number(e.target.value))}
                    style={{ width: '100%', accentColor: 'var(--accent)' }} />
                  <div style={{ display: 'flex', justifyContent: 'space-between',
                    fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: 2 }}>
                    <span>1 yr</span><span>10 yrs</span><span>20 yrs</span><span>40 yrs</span>
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                    <label style={{ margin: 0 }}>Expected Inflation Rate</label>
                    <span style={{ fontWeight: 800, color: '#ff4757', fontSize: '1.1rem' }}>
                      {inflation}%
                    </span>
                  </div>
                  <input type="range" min={2} max={12} step={0.5} value={inflation}
                    onChange={e => setInflation(Number(e.target.value))}
                    style={{ width: '100%', accentColor: '#ff4757' }} />
                  <div style={{ display: 'flex', justifyContent: 'space-between',
                    fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: 2 }}>
                    <span>2%</span><span>6% (avg)</span><span>12%</span>
                  </div>
                </div>

                {/* Live preview */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  <div style={{ background: 'var(--bg-secondary)', borderRadius: 10,
                    padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between' }}>
                    <div>
                      <div style={{ fontSize: '0.68rem', color: 'var(--text-secondary)' }}>TODAY'S TARGET</div>
                      <div style={{ fontWeight: 800, color: 'var(--accent)', fontSize: '1.1rem' }}>
                        ₹{target.toLocaleString('en-IN')}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '0.68rem', color: 'var(--text-secondary)' }}>
                        AFTER {years}Y INFLATION
                      </div>
                      <div style={{ fontWeight: 800, color: '#ff4757', fontSize: '1.1rem' }}>
                        ₹{Math.round(fv).toLocaleString('en-IN')}
                      </div>
                    </div>
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#ff4757', textAlign: 'center' }}>
                    ⚠️ Inflation will increase your need by ₹{Math.round(fv - target).toLocaleString('en-IN')}
                  </div>
                </div>
              </div>
            </div>

            <button className="btn btn-primary"
              style={{ marginTop: '1.25rem', width: '100%', padding: '13px', fontSize: '1rem' }}
              onClick={calculate} disabled={loading}>
              {loading
                ? <><div className="spinner-sm" /> Fetching live AMFI returns & calculating...</>
                : '📡 Calculate My SIP Plan with Live Data'}
            </button>
          </div>

          {/* ── RESULTS ── */}
          {result && (
            <>
              {/* Data source badge */}
              <div className="success-box" style={{ marginBottom: '1.25rem' }}>
                ✅ {result.profiles.Moderate.source} · Calculated at {new Date().toLocaleTimeString('en-IN')}
              </div>

              {/* STEP 3 — Choose Profile */}
              <div style={{ fontWeight: 700, color: 'var(--accent)', marginBottom: '0.75rem', fontSize: '1rem' }}>
                Step 3 — Choose Your Risk Profile
              </div>
              <div className="grid-3" style={{ marginBottom: '1.5rem' }}>
                {Object.entries(result.profiles).map(([profile, data]) => (
                  <ProfileCard key={profile} profile={profile} data={data}
                    selected={selProfile} onClick={() => setSelProfile(profile)} />
                ))}
              </div>

              {/* Selected profile detail */}
              {selData && (
                <div className="card" style={{ marginBottom: '1.25rem',
                  borderLeft: `4px solid ${PC[selProfile]}` }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between',
                    alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
                    <div>
                      <div style={{ fontWeight: 800, color: PC[selProfile], fontSize: '1.1rem' }}>
                        {PI[selProfile]} {selProfile} Plan Summary
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: 2 }}>
                        {PDESC[selProfile]}
                      </div>
                    </div>
                    <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
                      {[
                        { label: 'Monthly SIP',    val: `₹${selData.monthly_sip.toLocaleString('en-IN')}`, color: PC[selProfile] },
                        { label: 'Expected Return', val: `${selData.return_pct}% p.a.`,                    color: 'var(--accent)' },
                        { label: 'Total Invested',  val: `₹${(selData.total_invested/1e5).toFixed(1)}L`,   color: '#00d4ff' },
                        { label: 'Final Corpus',    val: `₹${(selData.total_value/1e5).toFixed(1)}L`,      color: '#00ff88' },
                        { label: 'Total Returns',   val: `₹${(selData.total_gain/1e5).toFixed(1)}L`,       color: '#ffa502' },
                      ].map(s => (
                        <div key={s.label} style={{ textAlign: 'center' }}>
                          <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)',
                            textTransform: 'uppercase', letterSpacing: '0.04em' }}>{s.label}</div>
                          <div style={{ fontWeight: 800, color: s.color, fontSize: '1rem' }}>{s.val}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* ── Charts Row 1 ── */}
              <div className="grid-2" style={{ marginBottom: '1rem' }}>
                <div className="card">
                  <PlotlyChart data={growthChart}
                    layout={{
                      title: 'SIP Growth Projection — All 3 Profiles',
                      height: 380,
                      yaxis: { title: '₹ Value', tickformat: ',.0f' },
                      xaxis: { title: 'Years' },
                      shapes: [{
                        type: 'line', x0: 0, x1: years, y0: fv, y1: fv,
                        line: { color: '#ff4757', dash: 'dash', width: 1.5 },
                      }],
                      annotations: [{
                        x: years * 0.5, y: fv,
                        text: `Target ₹${(fv / 1e5).toFixed(1)}L`,
                        showarrow: false, font: { color: '#ff4757', size: 11 },
                        yshift: 12,
                      }],
                    }} />
                </div>
                <div className="card">
                  <PlotlyChart data={inflationChart}
                    layout={{
                      title: `Inflation Impact at ${inflation}% p.a.`,
                      height: 380,
                      yaxis: { title: '₹ Required', tickformat: ',.0f' },
                      xaxis: { title: 'Years from Now' },
                    }} />
                </div>
              </div>

              {/* ── Charts Row 2 ── */}
              <div className="grid-2" style={{ marginBottom: '1rem' }}>
                <div className="card">
                  <PlotlyChart data={sipCompareBar}
                    layout={{
                      title: 'Monthly SIP Required by Risk Profile',
                      height: 320, bargap: 0.4,
                      yaxis: { title: '₹/month', tickformat: ',.0f' },
                    }} />
                </div>
                <div className="card">
                  <PlotlyChart data={corpusBar}
                    layout={{
                      title: 'Corpus Breakdown at Maturity',
                      height: 320, barmode: 'stack',
                      yaxis: { title: '₹', tickformat: ',.0f' },
                    }} />
                </div>
              </div>

              {/* ── Selected profile year-by-year ── */}
              {gainArea.length > 0 && (
                <div className="card" style={{ marginBottom: '1rem' }}>
                  <PlotlyChart data={gainArea}
                    layout={{
                      title: `${selProfile} Plan — Year-by-Year Growth`,
                      height: 320,
                      yaxis: { title: '₹', tickformat: ',.0f' },
                      xaxis: { title: 'Year' },
                      shapes: [{
                        type: 'line', x0: 0, x1: years, y0: fv, y1: fv,
                        line: { color: '#ff4757', dash: 'dash', width: 1.5 },
                      }],
                    }} />
                </div>
              )}

              {/* ── Fund Recommendations ── */}
              <div className="card" style={{ marginBottom: '1rem' }}>
                <div style={{ fontWeight: 700, color: 'var(--accent)', marginBottom: '1rem', fontSize: '1rem' }}>
                  🏦 Best Fund Recommendations for {selProfile} Profile
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)',
                    fontWeight: 400, marginLeft: 8 }}>
                    Live NAV & 3Y CAGR from AMFI + mfapi.in
                  </span>
                </div>
                {result.profiles[selProfile]?.funds?.length > 0 ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {result.profiles[selProfile].funds.map((fund, i) => (
                      <FundCard key={i} fund={fund} rank={i} />
                    ))}
                  </div>
                ) : (
                  <div className="info-box">
                    ℹ️ Fund data is being fetched from AMFI. Try recalculating.
                  </div>
                )}
              </div>

              {/* ── AI Advice ── */}
              {result.ai_advice && (
                <div className="card" style={{ marginBottom: '1rem',
                  borderLeft: '4px solid #a855f7',
                  background: 'linear-gradient(135deg,rgba(168,85,247,0.06),rgba(0,212,255,0.03))' }}>
                  <div style={{ fontWeight: 700, color: '#a855f7', marginBottom: '0.75rem',
                    display: 'flex', alignItems: 'center', gap: 8, fontSize: '1rem' }}>
                    🤖 AI Financial Advisor — Personalized Plan Analysis
                    <span className="badge badge-purple" style={{ fontSize: '0.65rem' }}>
                      Groq Llama 3.3 70B
                    </span>
                  </div>
                  <div style={{ color: 'var(--text-primary)', lineHeight: 1.85,
                    fontSize: '0.875rem', whiteSpace: 'pre-wrap' }}>
                    {result.ai_advice}
                  </div>
                </div>
              )}
              {!result.ai_advice && (
                <div className="warn-box" style={{ marginBottom: '1rem' }}>
                  ⚠️ AI advice unavailable — Add GROQ_API_KEY to .env for personalized AI analysis
                </div>
              )}

              {/* ── Save Goal ── */}
              <div className="card">
                <div style={{ fontWeight: 700, color: 'var(--accent)', marginBottom: '0.75rem' }}>
                  💾 Save This Goal to Dashboard
                </div>
                <div style={{ display: 'flex', gap: 12, alignItems: 'flex-end', flexWrap: 'wrap' }}>
                  <div style={{ flex: 1, minWidth: 180 }}>
                    <label>Risk Profile to Save</label>
                    <select value={saveProfile} onChange={e => setSaveProfile(e.target.value)}>
                      {['Conservative', 'Moderate', 'Aggressive'].map(p => (
                        <option key={p} value={p}>{PI[p]} {p} — ₹{result.profiles[p]?.monthly_sip?.toLocaleString('en-IN')}/mo</option>
                      ))}
                    </select>
                  </div>
                  <button className="btn btn-primary" style={{ padding: '10px 24px' }}
                    onClick={saveGoal}>
                    💾 Save Goal
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* ══════════════════════════════════════════════════════════
          TAB 2 — SAVED GOALS
      ══════════════════════════════════════════════════════════ */}
      {tab === 'goals' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between',
            alignItems: 'center', marginBottom: '1rem' }}>
            <div style={{ fontWeight: 700, color: 'var(--accent)' }}>
              Your Saved SIP Goals
            </div>
            <button className="btn btn-secondary" onClick={loadGoals}>🔄 Refresh</button>
          </div>

          {goals.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>🎯</div>
              <div style={{ fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                No goals saved yet
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
                Plan a SIP goal and save it to track your progress here
              </div>
              <button className="btn btn-primary" onClick={() => setTab('plan')}>
                🎯 Plan My First Goal
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {goals.map(g => {
                const fvG  = g.target_today * Math.pow(1 + g.inflation / 100, g.years);
                const col  = PC[g.risk_profile] || 'var(--accent)';
                const icon = GOAL_TYPES.find(t => t.id === g.goal_type)?.icon || '🎯';
                return (
                  <div key={g.id} className="card" style={{ borderLeft: `4px solid ${col}` }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between',
                      alignItems: 'flex-start', gap: 12 }}>
                      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                        <div style={{ fontSize: '2rem' }}>{icon}</div>
                        <div>
                          <div style={{ fontWeight: 800, fontSize: '1rem', color: col }}>
                            {g.goal_name}
                          </div>
                          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: 2 }}>
                            {g.risk_profile} · {g.years} years · {g.inflation}% inflation ·
                            {g.expected_return}% p.a. · Saved {new Date(g.created_at).toLocaleDateString('en-IN')}
                          </div>
                        </div>
                      </div>
                      <button className="btn btn-danger"
                        style={{ padding: '5px 12px', fontSize: '0.75rem' }}
                        onClick={() => deleteGoal(g.id)}>🗑️ Delete</button>
                    </div>

                    <div className="grid-5" style={{ marginTop: '1rem' }}>
                      {[
                        { label: "Today's Target",    val: `₹${g.target_today.toLocaleString('en-IN')}`,   color: 'var(--accent)' },
                        { label: 'Inflation-Adj Need', val: `₹${Math.round(fvG).toLocaleString('en-IN')}`, color: '#ff4757' },
                        { label: 'Monthly SIP',        val: `₹${g.monthly_sip.toLocaleString('en-IN')}`,   color: col },
                        { label: 'Time Horizon',       val: `${g.years} years`,                            color: 'var(--accent)' },
                        { label: 'Existing Savings',   val: `₹${(g.existing_savings || 0).toLocaleString('en-IN')}`, color: '#00ff88' },
                      ].map(r => (
                        <div key={r.label} style={{ textAlign: 'center', padding: '0.6rem',
                          background: 'var(--bg-secondary)', borderRadius: 8 }}>
                          <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)',
                            textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: 3 }}>
                            {r.label}
                          </div>
                          <div style={{ fontWeight: 800, color: r.color, fontSize: '0.9rem' }}>
                            {r.val}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
