import React, { useState, useRef, useEffect } from 'react';
import { ai } from '../api';

const QUICK = [
  { label: 'NIFTY Trend', q: 'What is the current NIFTY 50 trend and outlook?' },
  { label: 'Best Large Cap MF', q: 'What are the best large cap mutual funds in India right now?' },
  { label: 'IT Sector', q: 'Should I invest in the IT sector now? Pros and cons.' },
  { label: 'SIP vs Lump Sum', q: 'Explain SIP vs lump sum investment for a beginner.' },
  { label: 'FII/DII Impact', q: 'What is FII/DII and why does it matter for retail investors?' },
  { label: 'IPO Evaluation', q: 'How do I evaluate an IPO before applying? Key factors to check.' },
  { label: 'Sharpe Ratio', q: 'What is Sharpe Ratio and how to use it in portfolio management?' },
  { label: 'Best Sectors 2025', q: 'Which sectors are best to invest in for 2025 in India?' },
  { label: 'Tax Saving', q: 'Best tax saving investment options under Section 80C in India?' },
  { label: 'Gold vs Stocks', q: 'Should I invest in gold or stocks in the current market?' },
];

function Message({ msg }) {
  const isUser = msg.role === 'user';
  return (
    <div style={{ display:'flex', justifyContent: isUser ? 'flex-end' : 'flex-start',
      marginBottom: 12, animation: 'fadeIn 0.3s ease' }}>
      {!isUser && (
        <div style={{ width:32, height:32, borderRadius:'50%', background:'linear-gradient(135deg,#00d4ff,#00ff88)',
          display:'flex', alignItems:'center', justifyContent:'center',
          fontSize:'0.9rem', flexShrink:0, marginRight:8, marginTop:2 }}>🤖</div>
      )}
      <div className={isUser ? 'chat-bubble-user' : 'chat-bubble-ai'}>
        {!isUser && (
          <div style={{ fontSize:'0.65rem', color:'var(--accent)', fontWeight:700,
            marginBottom:5, letterSpacing:'0.05em' }}>AI ASSISTANT · GROQ LLAMA 3.3 70B</div>
        )}
        <div style={{ fontSize:'0.875rem', lineHeight:1.75, whiteSpace:'pre-wrap',
          color: isUser ? 'var(--text-primary)' : 'var(--text-primary)' }}>
          {msg.text}
        </div>
        <div style={{ fontSize:'0.65rem', color:'var(--text-muted)', marginTop:4, textAlign:'right' }}>
          {msg.time}
        </div>
      </div>
      {isUser && (
        <div style={{ width:32, height:32, borderRadius:'50%', background:'rgba(0,212,255,0.2)',
          display:'flex', alignItems:'center', justifyContent:'center',
          fontSize:'0.9rem', flexShrink:0, marginLeft:8, marginTop:2 }}>👤</div>
      )}
    </div>
  );
}

export default function AIAssistant() {
  const [messages, setMessages] = useState([{
    role: 'assistant',
    text: 'नमस्ते! 🙏 I\'m your AI Investment Assistant powered by Groq Llama 3.3 70B.\n\nI can help you with:\n• Indian stock market analysis\n• Mutual fund recommendations\n• IPO evaluation\n• Portfolio strategy\n• SIP planning\n• Market trends & news\n\nAsk me anything about investing in India!',
    time: new Date().toLocaleTimeString('en-IN', { hour:'2-digit', minute:'2-digit' }),
  }]);
  const [input,   setInput]   = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef  = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior:'smooth' }); }, [messages]);

  const send = async (question) => {
    const q = (question || input).trim();
    if (!q || loading) return;
    const time = new Date().toLocaleTimeString('en-IN', { hour:'2-digit', minute:'2-digit' });
    setMessages(m => [...m, { role:'user', text:q, time }]);
    setInput(''); setLoading(true);
    try {
      const r = await ai.chat(q);
      setMessages(m => [...m, {
        role:'assistant', text: r.data.answer || '❌ No response received.',
        time: new Date().toLocaleTimeString('en-IN', { hour:'2-digit', minute:'2-digit' }),
      }]);
    } catch (e) {
      setMessages(m => [...m, {
        role:'assistant', text:'❌ Connection error. Make sure the backend is running.',
        time: new Date().toLocaleTimeString('en-IN', { hour:'2-digit', minute:'2-digit' }),
      }]);
    } finally { setLoading(false); inputRef.current?.focus(); }
  };

  return (
    <div style={{ display:'flex', flexDirection:'column', height:'calc(100vh - 3.5rem)' }}>
      <div className="page-header">
        <div className="section-title">🤖 AI Investment Assistant</div>
        <div className="section-subtitle">
          <span className="pulse-dot"/>
          Groq Llama 3.3 70B · Indian market expert · Real-time context
        </div>
      </div>

      {/* Quick actions */}
      <div style={{ marginBottom:'1rem' }}>
        <div style={{ fontSize:'0.72rem', color:'var(--text-secondary)', marginBottom:6,
          textTransform:'uppercase', letterSpacing:'0.05em' }}>Quick Questions</div>
        <div style={{ display:'flex', gap:6, flexWrap:'wrap' }}>
          {QUICK.map((q, i) => (
            <button key={i} className="btn btn-secondary"
              style={{ fontSize:'0.72rem', padding:'5px 11px', borderRadius:20 }}
              onClick={() => send(q.q)} disabled={loading}>
              {q.label}
            </button>
          ))}
        </div>
      </div>

      {/* Chat window */}
      <div style={{ flex:1, overflowY:'auto', padding:'1rem',
        background:'var(--bg-secondary)', borderRadius:14,
        border:'1px solid var(--border)', marginBottom:'1rem',
        display:'flex', flexDirection:'column' }}>
        {messages.map((m, i) => <Message key={i} msg={m}/>)}
        {loading && (
          <div style={{ display:'flex', alignItems:'center', gap:8, padding:'8px 0' }}>
            <div style={{ width:32, height:32, borderRadius:'50%',
              background:'linear-gradient(135deg,#00d4ff,#00ff88)',
              display:'flex', alignItems:'center', justifyContent:'center', fontSize:'0.9rem' }}>🤖</div>
            <div className="chat-bubble-ai" style={{ display:'flex', gap:6, alignItems:'center' }}>
              <div className="spinner-sm"/>
              <span style={{ fontSize:'0.82rem', color:'var(--text-secondary)' }}>Thinking...</span>
            </div>
          </div>
        )}
        <div ref={bottomRef}/>
      </div>

      {/* Input */}
      <div style={{ display:'flex', gap:8 }}>
        <input ref={inputRef} value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send()}
          placeholder="Ask about stocks, mutual funds, IPOs, SIP, portfolio strategy..."
          style={{ flex:1, borderRadius:12, padding:'11px 16px' }}
          disabled={loading}/>
        <button className="btn btn-primary" onClick={() => send()}
          disabled={loading || !input.trim()}
          style={{ padding:'11px 20px', borderRadius:12, minWidth:80 }}>
          {loading ? <div className="spinner-sm"/> : 'Send ➤'}
        </button>
      </div>
      <div style={{ fontSize:'0.65rem', color:'var(--text-muted)', marginTop:5, textAlign:'center' }}>
        Powered by Groq Llama 3.3 70B · For educational purposes only · Not financial advice
      </div>
    </div>
  );
}
