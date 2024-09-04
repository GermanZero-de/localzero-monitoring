import Image from "next/image";
import Link from "next/link";
import { Col, Container, Row } from "react-bootstrap";
import Markdown from "react-markdown";
import greenCity from "@/public/background-green-city.png";
import LocalGroup from "@/app/components/LocalGroup";
import NavigationTile from "@/app/components/NavigationTile";
import styles from "./page.module.scss";
import { getCities } from "@/lib/dataService";
import indicator from "@/public/imgs/placeholders/indicator.png";
import indicator2 from "@/public/imgs/placeholders/indicator2.png";

interface CityDescriptionProps {
  teaser: string;
  description: string;
  name: string;
}

const CityDescription: React.FC<CityDescriptionProps> = ({ description, name, teaser }) => {
  if (!description) {
    return <></>;
  }
  return (
    <div className={styles.mdContent}>
      <h2 className="headingWithBar">Klimaschutz in {name}</h2>
      <h5>{teaser}</h5>
      <Markdown className="pb-3">{description}</Markdown>
    </div>
  );
};

interface SupportingNgosProps {
  supportingNgos: string;
}

const SupportingNgos: React.FC<SupportingNgosProps> = ({ supportingNgos }) => {
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

            <Link href={`${params.city}/massnahmen`} style={{ textDecoration: 'none' }}>
              <NavigationTile
                className={styles.tile}
                isBigCard
                title="Stand der Maßnahmen"
                subtitle="Umsetzung Klimaaktionsplan"
              >
                <div style={{height:300}}>
                <Image
                style={{padding:10, marginTop:70}}
                width={560}
                height={200}
                  src={indicator}
                  alt={"Fortschritt zur Klimaneutralität"}
                />
                </div>
              </NavigationTile>
            </Link>
          </div>
          <div className={styles.tileRowContainer}>
            <Link href={`${params.city}/kap_checkliste`} style={{ textDecoration: 'none' }}>
              <NavigationTile
                className={styles.tile}
                title="Klimaaktionsplan (KAP)"
              >
                <Image
                width={305}
                height={132}
                  src={indicator2}
                  alt={"Fortschritt zur Klimaneutralität"}
                />
              </NavigationTile>
            </Link>

            <Link href={`${params.city}/waermeplanung_checkliste`} style={{ textDecoration: 'none' }}>
              <NavigationTile
                className={styles.tile}
                title="Wärmeplanung"
              >
                  <Image
                width={305}
                height={132}
                  src={indicator2}
                  alt={"Fortschritt zur Klimaneutralität"}
                />
              </NavigationTile>
            </Link>

            <Link href={`${params.city}/verwaltungsstrukturen_checkliste`} style={{ textDecoration: 'none' }}>
              <NavigationTile
                className={styles.tile}
                title="Wo steht die Verwaltung?"

              >
                <Image
                width={305}
                height={132}
                  src={indicator2}
                  alt={"Fortschritt zur Klimaneutralität"}
                />
              </NavigationTile>
            </Link>

          </div>
        </div>
        <Row >
          <Col className="p-4">
            <CityDescription description={city.description} name={city.name} teaser={city.teaser}/>
          </Col>
        </Row>

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
            <p></p>
          </Col>
        </Row>
      </Container>

    </>
  );
}
