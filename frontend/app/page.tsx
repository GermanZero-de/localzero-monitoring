import { Container } from "react-bootstrap";
import { getCities } from "@/lib/dataService";
import { City } from "@/types";
import TileList from "./components/TileList";

export default async function Home() {
  const cities:City[] = await getCities();

  return (
    <>

      <Container>
        <h1 style={{ textAlign: "center" }}>LocalZero Monitoring</h1>
        <p className="block-text pb-3">
          ... ist eine Initiative von GermanZero, um mehr Transparenz zum Fortschritt der Klimaneutralität deutscher
          Kommunen zu schaffen. Der Fortschritt wird von ehrenamtlichen Lokalteams in den jeweiligen Kommunen regelmäßig
          aktualisiert.
        </p>
        <h2 className="headingWithBar">Kommunen im Monitoring</h2>

          <TileList cities={cities}></TileList>



      </Container>
    </>
  );
}
