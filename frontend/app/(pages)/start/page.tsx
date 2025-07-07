import { Container } from "react-bootstrap";
import { getCities } from "@/lib/dataService";
import { City } from "@/types";
import Subheader from "@/app/components/Subheader";
import TileList from "@/app/components/TileList";

export default async function Home() {
  const cities:City[] = await getCities();

  return (
    <>
      <Subheader />
      <Container>
        <div className="w-sm-75 m-auto">
          <h1 className="">Willkommen beim LocalMonitoring</h1>
          <p className="pb-4">
          Das LocalMonitoring ist eine Initiative von <a href="https://localzero.net/" target="new">LocalZero</a>. Ziel ist es, den Fortschritt deutscher Kommunen auf dem Weg zur Klimaneutralität transparent zu machen. Ehrenamtliche Lokalteams aktualisieren dafür regelmäßig die Daten in ihren jeweiligen Städten.
          </p>
        </div>

        <h1 className="headingWithBar">Kommunen im Monitoring</h1>

          <TileList cities={cities}></TileList>
      </Container>
    </>
  );
}
