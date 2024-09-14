import Image from "next/image";
import Link from "next/link";
import { Col, Container, Row } from "react-bootstrap";
import Markdown from "react-markdown";
import greenCity from "@/public/background-green-city.webp";
import LocalGroup from "@/app/components/LocalGroup";
import NavigationTile from "@/app/components/NavigationTile";
import styles from "./page.module.scss";
import { getCities, getTasks, getRecursiveStatusNumbers } from "@/lib/dataService";
import indicator2 from "@/public/imgs/placeholders/indicator2.png";
import ImplementationIndicator from "@/app/components/ImplementationIndicator";
import ChecklistIndicator from "@/app/components/ChecklistIndicator";
import { ChecklistItem } from "@/types";

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
  const tasks = await getTasks(params.city);
  if (!city || !tasks) {
    return <h3 className="pb-3 pt-3">Für die Stadt {params.city} gibt es kein Monitoring</h3>;
  }

  const kap = Array.isArray(city.cap_checklist) ? <Col className="p-2"><Link href={`${params.city}/kap_checkliste`} style={{ display:"inline-block", textDecoration: 'none' }}>
    <NavigationTile
      className={styles.tile}
      title="Klimaaktionsplan (KAP)"
    >
      <ChecklistIndicator
        total={city.cap_checklist.length}
        checked={city.cap_checklist.filter((item:ChecklistItem)=>item.is_checked).length}
        startYear={new Date(city.resolution_date).getFullYear()}
        endYear={city.target_year}
      />
    </NavigationTile>
  </Link></Col> : <></>

  const waerme = Array.isArray(city.energy_plan_checklist) ? <Col className="p-2"><Link href={`${params.city}/waermeplanung_checkliste`} style={{ display:"inline-block",textDecoration: 'none' }}>
    <NavigationTile
      className={styles.tile}
      title="Wärmeplanung"
    >
     <ChecklistIndicator
        total={city.energy_plan_checklist.length}
        checked={city.energy_plan_checklist.filter((item:ChecklistItem)=>item.is_checked).length}
        startYear={new Date(city.resolution_date).getFullYear()}
        endYear={city.target_year}
      />
    </NavigationTile>
  </Link></Col> : <></>

  const verwaltung = Array.isArray(city.assessment_administration) ? <Col className="p-2"><Link href={`${params.city}/verwaltungsstrukturen_checkliste`} style={{ display:"inline-block",textDecoration: 'none' }}>
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
  </Link></Col> : <></>
  return (
    <>
      <Container>
        <Row className="py-3">
          <Col className="d-flex flex-grow-1 py-2">
            <Link href={`#localgroup`} style={{ textDecoration: 'none', display: "flex", flex: 1 }}>
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
            </Link>
          </Col>
          <Col className="d-flex flex-grow-1 py-2">
            <Link href={`${params.city}/massnahmen`} style={{ textDecoration: 'none', display: "flex", flex: 1 }}>
              <NavigationTile
                className={styles.tile}
                isBigCard
                title="Stand der Maßnahmen"
                subtitle="Umsetzung Klimaaktionsplan"
              >
                <ImplementationIndicator
                  tasksNumber={getRecursiveStatusNumbers(tasks)}
                  startYear={new Date(city.resolution_date).getFullYear()}
                  endYear={city.target_year}
                />


              </NavigationTile>
            </Link>
          </Col>
        </Row>

        <Row className="py-3">
          {kap}
          {waerme}
          {verwaltung}
        </Row>

        <Row >
          <Col className="p-4">
            <CityDescription description={city.description} name={city.name} teaser={city.teaser} />
          </Col>
        </Row>

        <Row >
          <Col className="p-4" id="localgroup">
            <LocalGroup
              localGroup={city.local_group}
              isExpanded={false}
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
