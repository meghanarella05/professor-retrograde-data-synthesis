import React, {useMemo, useState} from "react";
import {createRoot} from "react-dom/client";
import {calculateKundli, capitalize, formatDegree, SIGN_SYMBOLS, type KundliResponse, type BirthDetails} from "@pos/shared";
import "./styles.css";

const API = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";

function App() {
  const [step,setStep] = useState(0);
  const [loading,setLoading] = useState(false);
  const [error,setError] = useState("");
  const [chart,setChart] = useState<KundliResponse|null>(null);
  const [birth,setBirth] = useState<BirthDetails>({
    date:"", time:"", latitude:12.9716, longitude:77.5946, timezone:"Asia/Kolkata"
  });

  const planets = useMemo(() => chart ? Object.entries(chart.planets) : [], [chart]);

  async function submit(e: React.FormEvent) {
    e.preventDefault(); setError(""); setLoading(true);
    try {
      const c = await calculateKundli(API,birth);
      setChart(c); setStep(1);
    } catch(err:any) { setError(err?.message ?? "Couldn't calculate the chart."); }
    finally { setLoading(false); }
  }

  if(step===0) return <Landing birth={birth} setBirth={setBirth} submit={submit} loading={loading} error={error}/>;
  return <Dashboard chart={chart!} reset={()=>{setStep(0);setChart(null)}} />;
}

function Shell({children}:{children:React.ReactNode}) {
  return <div className="app-shell">
    <header className="topbar"><div className="brand"><span className="brand-mark">✦</span><span>POS</span></div><span className="beta">PRIVATE BETA</span></header>
    {children}
  </div>
}

function Landing({birth,setBirth,submit,loading,error}:any) {
  return <Shell><main className="landing">
    <section className="hero">
      <div className="eyebrow">PERSONAL OPERATING SYSTEM</div>
      <h1>Understand the<br/><em>architecture</em> of you.</h1>
      <p className="hero-copy">A structured map of your personal operating patterns, built from your birth chart and a 20-dimensional trait model.</p>
      <form className="birth-card" onSubmit={submit}>
        <div className="card-label">YOUR BIRTH DETAILS</div>
        <div className="field-grid">
          <label>Date<input required type="date" value={birth.date} onChange={e=>setBirth({...birth,date:e.target.value})}/></label>
          <label>Time<input required type="time" step="1" value={birth.time} onChange={e=>setBirth({...birth,time:e.target.value})}/></label>
          <label>Latitude<input required type="number" step="0.000001" value={birth.latitude} onChange={e=>setBirth({...birth,latitude:Number(e.target.value)})}/></label>
          <label>Longitude<input required type="number" step="0.000001" value={birth.longitude} onChange={e=>setBirth({...birth,longitude:Number(e.target.value)})}/></label>
        </div>
        <label>Timezone<input required value={birth.timezone} onChange={e=>setBirth({...birth,timezone:e.target.value})}/></label>
        {error && <div className="error">{error}</div>}
        <button className="primary" disabled={loading}>{loading ? "Calculating…" : "Build my chart  →"}</button>
        <small>Uses sidereal calculations with Lahiri ayanamsa. Your chart is calculated locally through your connected backend.</small>
      </form>
    </section>
    <section className="manifesto">
      <div><span>01</span><h3>Not a single score.</h3><p>Twenty independent dimensions stay visible instead of being collapsed into one personality number.</p></div>
      <div><span>02</span><h3>Context changes expression.</h3><p>Planets, signs, houses and divisional charts act as transformation operators.</p></div>
      <div><span>03</span><h3>Designed to evolve.</h3><p>The calculation layer and interpretation layer stay separate, so the system can grow without breaking.</p></div>
    </section>
  </main></Shell>
}

function Dashboard({chart,reset}:{chart:KundliResponse,reset:()=>void}) {
  const [tab,setTab]=useState("overview");
  const asc=chart.ascendant;
  return <Shell><main className="dashboard">
    <aside className="sidebar">
      <div className="profile-orbit"><div className="orbit-ring"/><div className="orbit-core">{SIGN_SYMBOLS[asc.sign]}</div></div>
      <div className="asc-label">ASCENDANT</div><h2>{capitalize(asc.sign)}</h2><p>{formatDegree(asc.degree)}</p>
      <nav>{[["overview","Overview"],["planets","Planets"],["vargas","Vargas"],["bhava","Bhava Chalit"]].map(([id,label])=><button className={tab===id?"active":""} onClick={()=>setTab(id)} key={id}>{label}</button>)}</nav>
      <button className="reset" onClick={reset}>← New chart</button>
    </aside>
    <section className="content">
      <div className="content-head"><div><div className="eyebrow">YOUR CHART</div><h1>{tab==="overview"?"Personal Operating System":capitalize(tab)}</h1></div><div className="status-dot">● calculated</div></div>
      {tab==="overview" && <Overview chart={chart}/>}
      {tab==="planets" && <Planets planets={Object.entries(chart.planets)}/>}
      {tab==="vargas" && <Vargas chart={chart}/>}
      {tab==="bhava" && <Bhava chart={chart}/>}
    </section>
  </main></Shell>
}

function Overview({chart}:{chart:KundliResponse}) {
  const traits=["Openness","Conscientiousness","Extraversion","Curiosity","Achievement Drive","Creativity","Emotional Regulation","Resilience","Assertiveness","Empathy","Autonomy","Purpose Orientation"];
  return <div className="overview">
    <div className="intro-card"><div className="card-label">CORE IDEA</div><h2>Your chart is a map of <em>expression</em>, not a verdict.</h2><p>The POS engine keeps each trait independent and transforms it through chart context. This is the first layer of your profile.</p></div>
    <div className="section-title"><span>01</span><h2>Trait architecture</h2></div>
    <div className="trait-grid">{traits.map((t,i)=><div className="trait" key={t}><div className="trait-top"><span>{t}</span><b>{[62,48,71,84,66,77,55,69,73,61,82,88][i]}%</b></div><div className="bar"><i style={{width:`${[62,48,71,84,66,77,55,69,73,61,82,88][i]}%`}}/></div></div>)}</div>
    <div className="section-title"><span>02</span><h2>Planetary architecture</h2></div>
    <div className="planet-strip">{Object.entries(chart.planets).slice(0,7).map(([name,p]:any)=><div className="planet-chip" key={name}><span>{name}</span><b>{SIGN_SYMBOLS[p.sign]} {capitalize(p.sign)}</b><small>H{p.house} · {formatDegree(p.degree)}</small></div>)}</div>
  </div>
}

function Planets({planets}:{planets:any[]}) {
 return <div className="table-wrap"><table><thead><tr><th>Body</th><th>Sign</th><th>Degree</th><th>House</th><th>Motion</th></tr></thead><tbody>{planets.map(([name,p]:any)=><tr key={name}><td className="body">{name}</td><td>{SIGN_SYMBOLS[p.sign]} {capitalize(p.sign)}</td><td>{formatDegree(p.degree)}</td><td>House {p.house}</td><td>{p.retrograde?"Retrograde":"Direct"}</td></tr>)}</tbody></table></div>
}

function Vargas({chart}:{chart:KundliResponse}) {
 const entries=Object.entries(chart.divisional_charts);
 return <div><div className="varga-grid">{entries.map(([key,v]:any)=><div className="varga-card" key={key}><div><span className="varga-id">{key}</span><h3>{v.name}</h3></div><div className="mini-placements">{Object.entries(v.planets).slice(0,4).map(([body,p]:any)=><span key={body}>{body}: {SIGN_SYMBOLS[p.sign]} {capitalize(p.sign)}</span>)}</div></div>)}</div></div>
}

function Bhava({chart}:{chart:KundliResponse}) {
 const b:any=chart.bhava_chalit;
 return <div><div className="intro-card"><div className="card-label">BHAVA CHALIT · {b.method}</div><h2>Actual lived-house <em>expression</em>.</h2><p>The Chalit layer keeps house placement distinct from the whole-sign Rasi representation.</p></div><div className="table-wrap"><table><thead><tr><th>Body</th><th>Longitude</th><th>House</th></tr></thead><tbody>{Object.entries(b.planets||{}).map(([body,p]:any)=><tr key={body}><td className="body">{body}</td><td>{p.longitude.toFixed(4)}°</td><td>House {p.house}</td></tr>)}</tbody></table></div></div>
}

createRoot(document.getElementById("root")!).render(<App/>);
