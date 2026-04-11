import React, { useEffect, useState } from 'react';
import { news } from '../api';
import PlotlyChart from '../components/PlotlyChart';

const SENT_COLOR = {
  Positive: 'var(--accent-green)',
  Negative: 'var(--accent-red)',
  Neutral:  'var(--accent-orange)',
};

function NewsCard({ article }) {
  const sc = SENT_COLOR[article.sentiment?.label] || 'var(--text-secondary)';
  const score = article.sentiment?.score || 0;
  return (
    <div className="card" style={{ borderLeft:`3px solid ${sc}`, padding:'1rem' }}>
      <div style={{ display:'flex', justifyContent:'space-between', gap:12 }}>
        <div style={{ flex:1 }}>
          <a href={article.link} target="_blank" rel="noreferrer"
            style={{ fontWeight:600, fontSize:'0.875rem', color:'var(--text-primary)',
              textDecoration:'none', lineHeight:1.4, display:'block' }}
            onMouseEnter={e => e.target.style.color='var(--accent)'}
            onMouseLeave={e => e.target.style.color='var(--text-primary)'}>
            {article.title}
          </a>
          {article.summary && (
            <div style={{ fontSize:'0.78rem', color:'var(--text-secondary)', marginTop:5, lineHeight:1.5 }}>
              {article.summary.slice(0,160)}{article.summary.length>160?'...':''}
            </div>
          )}
          <div style={{ display:'flex', gap:10, marginTop:7, flexWrap:'wrap' }}>
            <span className="badge badge-blue" style={{ fontSize:'0.65rem' }}>📡 {article.source}</span>
            <span className="badge badge-purple" style={{ fontSize:'0.65rem' }}>🏷️ {article.category}</span>
            <span style={{ fontSize:'0.65rem', color:'var(--text-muted)' }}>
              🕐 {article.published?.slice(0,16)}
            </span>
          </div>
        </div>
        <div style={{ textAlign:'center', minWidth:64, flexShrink:0 }}>
          <div style={{ color:sc, fontWeight:800, fontSize:'0.82rem' }}>{article.sentiment?.label}</div>
          <div style={{ fontSize:'0.68rem', color:'var(--text-secondary)', marginTop:2 }}>
            {score > 0 ? '+' : ''}{score?.toFixed(3)}
          </div>
          <div style={{ marginTop:6 }}>
            <div style={{ width:48, height:4, background:'var(--border)', borderRadius:2, margin:'0 auto' }}>
              <div style={{ width:`${Math.abs(score)*100}%`, maxWidth:'100%', height:'100%',
                background:sc, borderRadius:2 }}/>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function NewsAndSentiment() {
  const [articles, setArticles]  = useState([]);
  const [sectors,  setSectors]   = useState({});
  const [loading,  setLoading]   = useState(true);
  const [filter,   setFilter]    = useState('All');
  const [tab,      setTab]       = useState('news');

  const load = () => {
    setLoading(true);
    Promise.all([news.live(60), news.sectorSentiment()])
      .then(([n, s]) => { setArticles(n.data.articles || []); setSectors(s.data); })
      .catch(console.error).finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const categories = ['All', ...new Set(articles.map(a => a.category).filter(Boolean))];
  const filtered = filter === 'All' ? articles : articles.filter(a => a.category === filter);

  const posCount = articles.filter(a => a.sentiment?.label === 'Positive').length;
  const negCount = articles.filter(a => a.sentiment?.label === 'Negative').length;
  const neuCount = articles.filter(a => a.sentiment?.label === 'Neutral').length;

  const sentPie = articles.length ? [{
    type:'pie',
    labels:['Positive','Negative','Neutral'],
    values:[posCount, negCount, neuCount],
    marker:{ colors:['#00ff88','#ff4757','#ffa502'], line:{color:'#060910',width:2} },
    hole:0.5, textinfo:'label+percent',
    textfont:{ color:'#f0f6fc', size:11 },
    hovertemplate:'<b>%{label}</b><br>%{value} articles<extra></extra>',
  }] : [];

  const sectorBar = Object.keys(sectors).length ? [{
    type:'bar',
    x: Object.keys(sectors),
    y: Object.values(sectors).map(s => s.score),
    marker:{ color: Object.values(sectors).map(s =>
      s.score > 0.05 ? 'rgba(0,255,136,0.7)' : s.score < -0.05 ? 'rgba(255,71,87,0.7)' : 'rgba(255,165,2,0.7)') },
    text: Object.values(sectors).map(s => s.label),
    textposition:'outside',
    hovertemplate:'<b>%{x}</b><br>Score: %{y:.3f}<br>%{text}<extra></extra>',
  }] : [];

  const scoreTimeline = articles.slice(0,30).reverse().map((a,i) => ({
    x: i, y: a.sentiment?.score || 0, label: a.title?.slice(0,40),
  }));
  const timelineChart = scoreTimeline.length ? [{
    type:'scatter', mode:'lines+markers',
    x: scoreTimeline.map(s=>s.x),
    y: scoreTimeline.map(s=>s.y),
    line:{ color:'#00d4ff', width:2 },
    marker:{ color: scoreTimeline.map(s => s.y > 0 ? '#00ff88' : s.y < 0 ? '#ff4757' : '#ffa502'), size:7 },
    fill:'tozeroy', fillcolor:'rgba(0,212,255,0.05)',
    hovertemplate:'<b>%{text}</b><br>Score: %{y:.3f}<extra></extra>',
    text: scoreTimeline.map(s=>s.label),
  }] : [];

  return (
    <div>
      <div className="page-header">
        <div className="section-title">📰 News & Sentiment Analysis</div>
        <div className="section-subtitle">
          <span className="pulse-dot"/>
          Live RSS feeds · TextBlob + VADER sentiment · {articles.length} articles
          <button className="btn btn-secondary" style={{ marginLeft:'auto', padding:'5px 12px', fontSize:'0.75rem' }}
            onClick={load}>🔄 Refresh</button>
        </div>
      </div>

      {/* KPIs */}
      {!loading && (
        <div className="grid-4" style={{ marginBottom:'1.25rem' }}>
          {[
            { label:'Total Articles', val:articles.length, color:'var(--accent)' },
            { label:'Positive',       val:posCount, color:'var(--accent-green)' },
            { label:'Negative',       val:negCount, color:'var(--accent-red)' },
            { label:'Neutral',        val:neuCount, color:'var(--accent-orange)' },
          ].map(k => (
            <div key={k.label} className="kpi-card" style={{ borderLeftColor:k.color }}>
              <div className="kpi-label">{k.label}</div>
              <div className="kpi-value" style={{ color:k.color }}>{k.val}</div>
            </div>
          ))}
        </div>
      )}

      <div className="tab-bar">
        {[['news','📰 Live News'],['sentiment','📊 Sentiment Analysis']].map(([id,label])=>(
          <button key={id} className={`tab ${tab===id?'active':''}`} onClick={()=>setTab(id)}>{label}</button>
        ))}
      </div>

      {loading && <div className="loading"><div className="spinner"/><div className="loading-text">Fetching live news...</div></div>}

      {tab === 'news' && !loading && (
        <>
          <div style={{ display:'flex', gap:6, marginBottom:'1rem', flexWrap:'wrap' }}>
            {categories.map(c => (
              <button key={c} className={`btn ${filter===c?'btn-primary':'btn-secondary'}`}
                style={{ padding:'5px 12px', fontSize:'0.75rem', borderRadius:20 }}
                onClick={() => setFilter(c)}>{c}</button>
            ))}
          </div>
          <div style={{ display:'flex', flexDirection:'column', gap:8 }}>
            {filtered.map((a, i) => <NewsCard key={i} article={a}/>)}
          </div>
        </>
      )}

      {tab === 'sentiment' && !loading && (
        <div style={{ display:'flex', flexDirection:'column', gap:'1rem' }}>
          <div className="grid-2">
            <div className="card">
              <PlotlyChart data={sentPie}
                layout={{ title:'Sentiment Distribution', height:360, showlegend:true,
                  annotations:[{ text:`<b>${articles.length}</b><br>articles`,
                    x:0.5, y:0.5, showarrow:false, font:{color:'#f0f6fc',size:13} }] }}/>
            </div>
            <div className="card">
              <PlotlyChart data={timelineChart}
                layout={{ title:'Sentiment Score Timeline (latest 30 articles)', height:360,
                  yaxis:{title:'Sentiment Score', zeroline:true, zerolinecolor:'#30363d'},
                  xaxis:{title:'Article Index (newest right)'} }}/>
            </div>
          </div>
          <div className="card">
            <PlotlyChart data={sectorBar}
              layout={{ title:'Sector Sentiment Score (positive = bullish news)', height:360,
                yaxis:{title:'Sentiment Score'},
                shapes:[{type:'line',x0:-0.5,x1:Object.keys(sectors).length-0.5,y0:0,y1:0,
                  line:{color:'#30363d',dash:'dash'}}] }}/>
          </div>
          <div className="grid-3">
            {Object.entries(sectors).map(([sector, data]) => {
              const c = SENT_COLOR[data.label] || 'var(--text-secondary)';
              return (
                <div key={sector} className="card" style={{ borderLeft:`3px solid ${c}` }}>
                  <div style={{ fontWeight:700, color:'var(--accent)', marginBottom:4 }}>{sector}</div>
                  <div style={{ color:c, fontWeight:800, fontSize:'1.1rem' }}>{data.label}</div>
                  <div style={{ fontSize:'0.75rem', color:'var(--text-secondary)', marginTop:3 }}>
                    Score: {data.score > 0 ? '+' : ''}{data.score?.toFixed(3)} · {data.count} articles
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
