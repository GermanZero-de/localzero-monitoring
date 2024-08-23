import Search from "@/app/components/Search";
import Image from "next/image";
import Link from "next/link";
import { Container } from "react-bootstrap";
import banner from "../public/images/dashboard-banner.jpg";
import Tile from "./components/Tile";
import styles from "./page.module.scss";
import CallToActionTile from "@/app/components/CallToActionTile";

import expandArrowUp from "@/public/images/arrow-expand-up.svg";
import expandArrowDown from "@/public/images/arrow-expand-down.svg";

import { getCities } from "@/lib/dataService";
import { City } from "@/types";

export default async function Home() {
  const cities= await getCities();
  const numberOfCitiesShown = 4;
  const allCitiesShown= false;

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
        <h2 className="headingWithBar">Kommunen im Monitoring</h2>
        <div className="d-flex justify-content-between flex-wrap">
          {(cities || []).slice(0, numberOfCitiesShown).map((city:City) => (
            <Link
              key={city.slug}
              href={"/" + city.slug}
              className={styles.noLinkStyling}
            >
              <Tile
                name={city.name}
                logo={city.local_group?.logo}
              />
            </Link>
          ))}
        </div>
        <div className="block-text pb-3">
          {!allCitiesShown ? <div>Anzeige weiterer Kommunen</div> : <></>}
          <Image
            src={allCitiesShown ? expandArrowUp : expandArrowDown}
            alt="Zeige mehr über das Lokalteam"
          />
        </div>
        <h2 className="headingWithBar">Entdecke lokalen Klimaschutz</h2>
        <Search cities={cities} />
        <h2 className="headingWithBar">
          LocalMonitoring wird ehrenamtlich von engagierten Bürger:innen der jeweiligen Stadt betrieben.
        </h2>
        <div className={styles.callToActionSection}>
          <CallToActionTile
            title="Schreibe uns eine Mail:"
            text="localzero@germanzero.de"
            link="mailto:localzero@germanzero.de"
            type="contact"
          />
          <CallToActionTile
            title="Du willst mitmachen?"
            link="https://localzero.net/mitmachen"
            type="join"
          />
        </div>
      </Container>
    </>
  );
}
