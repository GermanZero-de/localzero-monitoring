import Image from "next/image";
import banner from "../public/images/dashboard-banner.jpg";
import styles from "./page.module.scss";
import { Container } from "react-bootstrap";
import { db } from "./db/db.server";
import { cpmonitorCity } from "./db/schema";
import Tile from "./components/Tile"

const getCities = async()=> {
  const cities = await db.select().from(cpmonitorCity);
  console.log(cities)
  return cities;
}

export default async function Home() {
  const all_cities = await getCities();
  return (
    <>
      <div className={styles.banner}>
        <h1 className={styles.textPrimary}>Auf dem Weg zur Klimaneutralität</h1>
        <h1 className={styles.textSecondary}>Klimaschutz-Monitoring von Kommunen</h1>

        <Image
          fill
          style={{ objectFit: "cover" }}
          src={banner}
          alt="Fröhliches Kind mit Strohhut in einer grünen Stadt"
        />
      </div>
      <Container>
        <h1 style={{ textAlign: "center" }}>LocalZero Monitoring</h1>
        <p className="block-text pb-3">
          ... ist eine Initiative von GermanZero, um mehr Transparenz zum Fortschritt der Klimaneutralität deutscher
          Kommunen zu schaffen. Der Fortschritt wird von ehrenamtlichen Lokalteams in den jeweiligen Kommunen regelmäßig
          aktualisiert.
        </p>
        <h2>Kommunen im Monitoring</h2>
        <div className="d-flex justify-content-between flex-wrap">{all_cities.map(city=>(<Tile name={city.name} />))}</div>
        <h2>Entdecke lokalen Klimaschutz</h2>
        <p className="pb-3">TODO: Suche</p>
        <h2>LocalMonitoring wird ehrenamtlich von engagierten Bürger:innen der jeweiligen Stadt betrieben.</h2>
        <p className="pb-3">TODO: call to action tiles</p>
      </Container>
    </>
  );
}
