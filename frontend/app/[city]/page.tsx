import Image from "next/image";
import Link from "next/link";
import { Col, Container, Row } from "react-bootstrap";
import Markdown from "react-markdown";
import arrow from "../../public/images/arrow-right-down.svg";
import greenCity from "../../public/background-green-city.png";
import LocalGroup from "../components/LocalGroup";
import NavigationTile from "@/app/components/NavigationTile";
import styles from "./page.module.scss";
import { getCities } from "@/lib/dataService";

interface CityDescriptionProps {
  description: string;
}

const CityDescription: React.FC<CityDescriptionProps> = ({ description }) => {
  if (!description) {
    return <></>;
  }
  return (
    <>
      <h2 className="headingWithBar">Klimaschutz in München</h2>
      <Markdown className="block-text pb-3">{description}</Markdown>
    </>
  );
};

interface SupportingNgosProps {
  supportingNgos: string;
}

const SupportingNgos: React.FC<SupportingNgosProps>  = ({ supportingNgos }) => {
  if (!supportingNgos) {
    return <></>;
  }
  return (
    <>
      <h2 className="headingWithBar">Mit Unterstützung von</h2>
      <Markdown className="block-text pb-3">{supportingNgos}</Markdown>
    </>
  );
};
export default async function CityDashboard({ params }: { params: { city: string } }) {
  const city = await getCities(params.city);
  if (!city) {
    return <h3 className="pb-3 pt-3">Für die Stadt {params.city} gibt es kein Monitoring</h3>;
  }

  return (
    <>
      <Container>
        <h1 style={{ fontWeight: 600, fontSize: 38 }}>
          {city.name.toUpperCase()}
          <Image
            src={arrow}
            alt=""
          />
        </h1>
        <div className="p-3">
          <div className={styles.tileRowContainer}>

              <NavigationTile
                className={styles.tile}
                isBigCard
                title={"Alles klar in " + city.name + "?"}
                subtitle="Einleitung"
              >
                <Image
                  style={{ width: "100%", height: "100%" }}
                  src={greenCity}
                  alt=""
                />
              </NavigationTile>

            <Link href={`${params.city}/massnahmen`}>
              <NavigationTile
                className={styles.tile}
                isBigCard
                title="Stand der Maßnahmen"
                subtitle="Umsetzung Klimaaktionsplan"
              >
                <span>Bild</span>
              </NavigationTile>
            </Link>
          </div>
          <div className={styles.tileRowContainer}>
          <Link href={`${params.city}/kap_checkliste`}>
            <NavigationTile
              className={styles.tile}
              title="Klimaaktionsplan (KAP)"
            >
                  <span>Bild</span>
            </NavigationTile>
            </Link>

            <NavigationTile
              className={styles.tile}
              title="Wärmeplanung"
            >
              <span>Bild</span>
            </NavigationTile>
            <NavigationTile
              className={styles.tile}
              title="Wo steht die Verwaltung?"

            >
              <span>Bild</span>
            </NavigationTile>
          </div>
        </div>
        <CityDescription description={city.description} />
        <Row >
          <Col className="p-4">
            <LocalGroup
              localGroup={city.local_group}
              isExpanded={true}
            />
          </Col>
        </Row>
        <Row >
          <Col className="p-4">
            <SupportingNgos supportingNgos={city.supporting_ngos} />
          </Col>
        </Row>
        <Row >
          <Col className="p-4">
            <p>{JSON.stringify(city)}</p>
          </Col>
        </Row>
      </Container>

    </>
  );
}
