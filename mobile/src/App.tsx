import React,{useState} from "react";
import {SafeAreaView,View,Text,TextInput,Pressable,ScrollView,StyleSheet,ActivityIndicator} from "react-native";
import {calculateKundli,capitalize,SIGN_SYMBOLS,formatDegree,type BirthDetails,KundliResponse} from "@pos/shared";

const API = process.env.EXPO_PUBLIC_API_BASE ?? "http://127.0.0.1:8000";
const A="#d7b58a", BG="#0d0c0b", PANEL="#151311", LINE="#2c2824", MUTED="#918a80", INK="#eee9df";

export default function App(){
 const [chart,setChart]=useState<KundliResponse|null>(null);
 const [loading,setLoading]=useState(false); const [error,setError]=useState("");
 const [birth,setBirth]=useState<BirthDetails>({date:"",time:"",latitude:12.9716,longitude:77.5946,timezone:"Asia/Kolkata"});
 async function go(){setLoading(true);setError("");try{setChart(await calculateKundli(API,birth))}catch(e:any){setError(e?.message??"Couldn't calculate chart.")}finally{setLoading(false)}}
 if(chart) return <ChartScreen chart={chart} reset={()=>setChart(null)}/>;
 return <SafeAreaView style={s.safe}><ScrollView contentContainerStyle={s.page}>
  <Text style={s.mark}>✦  POS</Text><Text style={s.kicker}>PERSONAL OPERATING SYSTEM</Text>
  <Text style={s.hero}>Understand the <Text style={s.italic}>architecture</Text> of you.</Text>
  <Text style={s.copy}>A structured map of your personal operating patterns, built from your birth chart and a 20-dimensional trait model.</Text>
  <View style={s.card}><Text style={s.label}>YOUR BIRTH DETAILS</Text>
   <Field label="Date" value={birth.date} placeholder="YYYY-MM-DD" onChangeText={(v:string)=>setBirth({...birth,date:v})}/>
   <Field label="Time" value={birth.time} placeholder="HH:MM:SS" onChangeText={(v:string)=>setBirth({...birth,time:v})}/>
   <Field label="Latitude" value={String(birth.latitude)} onChangeText={(v:string)=>setBirth({...birth,latitude:Number(v)})}/>
   <Field label="Longitude" value={String(birth.longitude)} onChangeText={(v:string)=>setBirth({...birth,longitude:Number(v)})}/>
   <Field label="Timezone" value={birth.timezone} onChangeText={(v:string)=>setBirth({...birth,timezone:v})}/>
   {error?<Text style={s.error}>{error}</Text>:null}
   <Pressable style={s.button} onPress={go} disabled={loading}>{loading?<ActivityIndicator color="#17130f"/>:<Text style={s.buttonText}>Build my chart  →</Text>}</Pressable>
  </View>
  <Text style={s.foot}>Sidereal · Lahiri · POS v0.1</Text>
 </ScrollView></SafeAreaView>
}

function Field({label,value,onChangeText,placeholder}:{label:string,value:string,onChangeText:(v:string)=>void,placeholder?:string}){
 return <View style={{marginTop:16}}><Text style={s.fieldLabel}>{label}</Text><TextInput style={s.input} value={value} placeholder={placeholder} placeholderTextColor="#57524d" onChangeText={onChangeText}/></View>
}

function ChartScreen({chart,reset}:{chart:KundliResponse,reset:()=>void}){
 const [tab,setTab]=useState("overview");
 const tabs=["overview","planets","vargas"];
 return <SafeAreaView style={s.safe}><ScrollView contentContainerStyle={s.page}>
  <View style={s.row}><Text style={s.mark}>✦  POS</Text><Pressable onPress={reset}><Text style={s.muted}>New chart</Text></Pressable></View>
  <View style={s.asc}><Text style={s.symbol}>{SIGN_SYMBOLS[chart.ascendant.sign]}</Text><Text style={s.kicker}>ASCENDANT</Text><Text style={s.title}>{capitalize(chart.ascendant.sign)}</Text><Text style={s.muted}>{formatDegree(chart.ascendant.degree)}</Text></View>
  <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{marginVertical:24}}>{tabs.map(t=><Pressable key={t} onPress={()=>setTab(t)} style={[s.tab,tab===t&&s.tabActive]}><Text style={[s.tabText,tab===t&&{color:INK}]}>{capitalize(t)}</Text></Pressable>)}</ScrollView>
  {tab==="overview"?<MobileOverview chart={chart}/>:tab==="planets"?<MobilePlanets chart={chart}/>:<MobileVargas chart={chart}/>}
 </ScrollView></SafeAreaView>
}

function MobileOverview({chart}:{chart:KundliResponse}){
 const vals=[62,48,71,84,66,77,55,69,73,61,82,88], names=["Openness","Conscientiousness","Extraversion","Curiosity","Achievement Drive","Creativity","Emotional Regulation","Resilience","Assertiveness","Empathy","Autonomy","Purpose Orientation"];
 return <><View style={s.card}><Text style={s.label}>CORE IDEA</Text><Text style={s.h2}>Your chart is a map of <Text style={s.italic}>expression</Text>, not a verdict.</Text><Text style={s.copy}>Twenty independent dimensions remain visible instead of collapsing everything into one score.</Text></View><Text style={s.section}>TRAIT ARCHITECTURE</Text>{names.map((n,i)=><View style={s.trait} key={n}><View style={s.row}><Text style={s.fieldLabel}>{n}</Text><Text style={s.accent}>{vals[i]}%</Text></View><View style={s.bar}><View style={[s.barFill,{width:`${vals[i]}%`}]}/></View></View>)}</>
}
function MobilePlanets({chart}:{chart:KundliResponse}){return <View>{Object.entries(chart.planets).map(([n,p]:any)=><View style={s.planet} key={n}><Text style={s.h3}>{n}</Text><Text style={s.muted}>{SIGN_SYMBOLS[p.sign]} {capitalize(p.sign)} · {formatDegree(p.degree)} · H{p.house}</Text><Text style={s.small}>{p.retrograde?"Retrograde":"Direct"}</Text></View>)}</View>}
function MobileVargas({chart}:{chart:KundliResponse}){return <View>{Object.entries(chart.divisional_charts).map(([k,v]:any)=><View style={s.planet} key={k}><Text style={s.accent}>{k}</Text><Text style={s.h3}>{v.name}</Text><Text style={s.muted}>{Object.entries(v.planets).slice(0,3).map(([b,p]:any)=>`${b}: ${capitalize(p.sign)}`).join("  ·  ")}</Text></View>)}</View>}

const s=StyleSheet.create({
 safe:{flex:1,backgroundColor:BG},page:{padding:24,paddingBottom:60},mark:{color:INK,fontWeight:"700",letterSpacing:3,fontSize:15},kicker:{color:MUTED,fontSize:10,letterSpacing:2.2,marginTop:42},hero:{color:INK,fontSize:46,lineHeight:48,fontWeight:"600",marginTop:14,letterSpacing:-1.8},italic:{fontStyle:"italic",fontFamily:"serif",color:A},copy:{color:"#aaa198",fontSize:14,lineHeight:24,marginTop:18},card:{backgroundColor:PANEL,borderWidth:1,borderColor:LINE,padding:22,marginTop:30},label:{color:MUTED,fontSize:10,letterSpacing:2},fieldLabel:{color:"#aaa198",fontSize:11},input:{backgroundColor:"#0f0e0d",borderWidth:1,borderColor:LINE,color:INK,padding:12,marginTop:7},button:{backgroundColor:A,padding:15,alignItems:"center",marginTop:24},buttonText:{color:"#17130f",fontWeight:"700"},error:{color:"#df8e7b",fontSize:11,marginTop:12},foot:{color:"#57524d",fontSize:10,marginTop:30},row:{flexDirection:"row",justifyContent:"space-between",alignItems:"center"},muted:{color:MUTED,fontSize:11},asc:{alignItems:"center",paddingTop:35},symbol:{fontSize:62,color:A},title:{fontSize:28,color:INK,fontWeight:"600",marginTop:7},tab:{paddingVertical:10,paddingHorizontal:15,borderWidth:1,borderColor:LINE,marginRight:8},tabActive:{backgroundColor:PANEL,borderColor:"#493f34"},tabText:{color:MUTED,fontSize:11},h2:{fontSize:24,lineHeight:31,color:INK,fontWeight:"600",marginTop:12},h3:{fontSize:14,color:INK,fontWeight:"600",marginTop:5},section:{color:MUTED,fontSize:10,letterSpacing:2,marginTop:38,marginBottom:18},trait:{marginBottom:18},accent:{color:A,fontSize:11},bar:{height:3,backgroundColor:"#292521",marginTop:8},barFill:{height:3,backgroundColor:A},planet:{borderWidth:1,borderColor:LINE,backgroundColor:PANEL,padding:17,marginBottom:9},small:{color:"#6f6962",fontSize:9,marginTop:7}
});
