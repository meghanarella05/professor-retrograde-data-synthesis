export const TRAITS = [
  ["O", "Openness"], ["C", "Conscientiousness"], ["E", "Extraversion"],
  ["A", "Agreeableness"], ["ES", "Emotional Stability"], ["Cur", "Curiosity"],
  ["AD", "Achievement Drive"], ["D", "Discipline"], ["Cr", "Creativity"],
  ["Ad", "Adaptability"], ["ER", "Emotional Regulation"], ["R", "Resilience"],
  ["As", "Assertiveness"], ["Em", "Empathy"], ["Att", "Attachment Security"],
  ["RT", "Risk Tolerance"], ["Au", "Autonomy"], ["P", "Purpose Orientation"],
  ["ST", "Systems Thinking"], ["SC", "Self-Control"],
] as const;

export type TraitKey = typeof TRAITS[number][0];

export type BirthDetails = {
  date: string;
  time: string;
  latitude: number;
  longitude: number;
  timezone: string;
};

export type KundliResponse = {
  ayanamsa: string;
  ascendant: { sign: string; longitude: number; degree: number };
  planets: Record<string, {
    sign: string; degree: number; longitude: number; house: number; retrograde: boolean
  }>;
  houses: Record<string, { sign: string }>;
  divisional_charts: Record<string, unknown>;
  bhava_chalit: Record<string, unknown>;
  metadata: Record<string, unknown>;
};

export const SIGN_SYMBOLS: Record<string, string> = {
  aries:"♈", taurus:"♉", gemini:"♊", cancer:"♋", leo:"♌", virgo:"♍",
  libra:"♎", scorpio:"♏", sagittarius:"♐", capricorn:"♑", aquarius:"♒", pisces:"♓"
};

export const capitalize = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

export function formatDegree(deg: number) {
  const d = Math.floor(deg);
  const m = Math.round((deg - d) * 60);
  return `${d}° ${m.toString().padStart(2, "0")}'`;
}

export async function calculateKundli(apiBase: string, birth: BirthDetails): Promise<KundliResponse> {
  const res = await fetch(`${apiBase.replace(/\/$/, "")}/kundli/calculate`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(birth),
  });
  if (!res.ok) throw new Error(`Kundli request failed (${res.status})`);
  return res.json();
}
