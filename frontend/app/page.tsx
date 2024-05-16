import Image from "next/image";
import banner from "../public/dashboard-banner.jpg";
import styles from "./page.module.scss";
import { Container } from "react-bootstrap";

export default function Home() {
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
        <p className="pb-3">TODO: Kommunen</p>
        <h2>Entdecke lokalen Klimaschutz</h2>
        <p className="pb-3">TODO: Suche</p>
        <h2>LocalMonitoring wird ehrenamtlich von engagierten Bürger:innen der jeweiligen Stadt betrieben.</h2>
        <p className="pb-3">TODO: call to action tiles</p>
      </Container>
    </>
  );
}
