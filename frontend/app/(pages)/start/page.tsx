import { Container } from "react-bootstrap";
import { getCities } from "@/lib/dataService";
import { City } from "@/types";
import TileList from "@/app/components/TileList";

export default async function Home() {
  const cities:City[] = await getCities();

  return (
    <>

      <Container>
        <h1 className="py-4 w-sm-75 m-auto">LocalMonitoring</h1>
        <p className="pb-5 w-sm-75 m-auto">
        ... ist eine Initiative von <a href="https://localzero.net/" target="new">LocalZero</a>, um mehr Transparenz zum Fortschritt der Klimaneutralität deutscher Kommunen zu schaffen. Der Fortschritt wird von ehrenamtlichen Lokalteams in den jeweiligen Kommunen regelmäßig aktualisiert.
        </p>
        <h1 className="headingWithBar">Kommunen im Monitoring</h1>

          <TileList cities={cities}></TileList>



      </Container>
    </>
  );
}
