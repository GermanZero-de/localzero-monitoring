
import Search from "@/app/components/Search";
import styles from "./styles/Footer.module.scss";
import CallToActionTile from "@/app/components/CallToActionTile";

import { City } from "@/types";
import { Container } from "react-bootstrap";
type Props = {
  cities: City[];
};

const Subfooter: React.FC<Props> = ({ cities }) => {
  return (
    <Container>
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
  );
}

export default Subfooter;
