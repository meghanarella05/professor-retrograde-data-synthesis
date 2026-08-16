export type BirthDetails = {
  birth_date: string;
  birth_time: string;
  timezone_offset: number;
  place?: string;
  latitude?: number;
  longitude?: number;
};

export async function fetchFullChart(baseUrl: string, details: BirthDetails) {
  const response = await fetch(`${baseUrl}/api/chart/full`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(details),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch chart: ${response.status}`);
  }

  return response.json();
}
