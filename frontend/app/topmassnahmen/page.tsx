import { db } from "../db/db.server";
import { cpmonitorCity } from "../db/schema";
import { Container } from "react-bootstrap";

async function getCities() {
  const cities = await db.select().from(cpmonitorCity);
  return cities;
}

export default async function TopMassnahmen() {
  const all_cities = await getCities();
  return (
    <Container className="min-vh-50 p-3">
      LocalZero hat dafür einige Studien und viele Klima-Aktionspläne ausgewertet und die Maßnahmen unter folgenden
      Gesichtspunkten zusammengestellt: Impact auf Treibhausgaseinsparung technische Umsetzbarkeit derzeit möglich
      Umsetzung kommunal möglich ein überschaubarer Kreis von Akteuren (z.B. Eigenbetriebe, Politik und Verwaltung)
      Wirtschaftlichkeit (z.B. PV auf kommunalen Dächern) Priorisierung Priorität A (inklusive der 15 Startmaßnahmen)
      Maßnahmen mit hoher Treibhausgaseinsparung, die schnell umsetzbar sind, gute Startmaßnahmen in der Kommunikation
      mit Verwaltung und Politik: "das Dringende zuerst" Priorität B: Maßnahmen mit etwas niedriger
      Treibhausgaseinsparung: "der nächste Schritt" Priorität A und B: Sind gute Schritte in Richtung Klimaneutralität,
      es braucht aber noch weitere nötige Maßnahmen! Mehr Informationen zu Klima-Aktionsplänen: Im LocalZero-Wiki
      findest du die Mindestanforderungen an einen guten Klima-Aktionsplan: LocalZero:Klima-Aktionsplan.
    </Container>
  );
}
