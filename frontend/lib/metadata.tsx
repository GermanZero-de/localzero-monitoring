import type { Metadata } from 'next';
import { getCities } from '@/lib/dataService';

export async function generateMetadataForCity(cityName: string): Promise<Metadata> {
  const city = await getCities(cityName);
  return {
    title: `LocalZero Monitoring - ${city.name}`,
    description: `Monitoring von Klimaschutz-Maßnahmen in ${city}`,
  };
}