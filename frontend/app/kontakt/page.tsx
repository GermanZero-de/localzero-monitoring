import { Container } from "react-bootstrap";
import Search from "@/app/components/Search";
import styles from "@/app/page.module.scss";
import CallToActionTile from "@/app/components/CallToActionTile";
import { getCities } from "@/lib/dataService";
import type { City } from "@/types";
export default async function ProjectDescription() {
  const cities:City[] = await getCities();

  return (
    <Container>
      <h1 className="big-h1">Kontakt</h1>
      <div className="pb-3">
        Wir haben uns bemüht die Informationen und die Website sehr klar aufzubereiten, aber es ergeben sich immer Fragen. Darum scheue nicht uns zu kontaktieren ...
      </div>
      <h2 className="headingWithBar">Monitoring</h2>
      <div className="pb-3">
         Philipp beantwortet dir alle Fragen zum Monitoring, zur Website... Bitte schicke eine E-Mail oder vereinbare einen Termin
      </div>
      <h2 className="headingWithBar">Lokalteams</h2>
      <div className="pb-3">
      Leonie beantwortet dir alle Fragen zu den Lokalteams... Bitte schicke eine E-Mail oder vereinbare einen Termin
      </div>
      <h2 className="headingWithBar">Maßnahmen</h2>
      <div className="pb-3">
      Johannes beantwortet dir alle Fragen zu den Maßnahmen... Bitte schicke eine E-Mail oder vereinbare einen Termin
      </div>
    </Container>
  );
}
