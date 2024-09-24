
import "bootstrap-icons/font/bootstrap-icons.css";
import { Accordion, Container } from "react-bootstrap";
import ChecklistItem from "@/app/components/ChecklistItem";
import { getCities } from "@/lib/dataService";
import ChecklistIndicator from "@/app/components/ChecklistIndicator";
import { CheckItem } from "@/types";

export default async function EnergyPlanChecklist({ params }: { params: { city: string } }) {
  const city = await getCities(params.city);

  if (!city) {
    return <h3 className="pb-3 pt-3">Für die Stadt {params.city} gibt es kein Monitoring</h3>;
  }

  return (
    <>
      <Container className="w-sm-75">
      <div className="pb-3">
          <ChecklistIndicator
            style={{height:250, marginBottom:30}}
            total={city.energy_plan_checklist.length}
            checked={city.energy_plan_checklist.filter((item: CheckItem) => item.is_checked).length}
            startYear={new Date(city.resolution_date).getFullYear()}
            endYear={city.target_year}
            showLegend
            title="Wie steht es um die Wärmeplanung?"
          /></div>
        <h1 className="headingWithBar">Wärmeplanung</h1>
        <div className="pb-4">
          Der Wärmewende kommt eine Schlüsselposition bei der Einhaltung des Paris Agreement und damit der Begrenzung
          der Klimaerhitzung auf unter 2 Grad zu. Im Stromsektor gibt es etablierte Marktmechanismen, im Verkehrssektor
          sind die Lösungen bekannt, im Wärmesektor hingegen müssen Lösungen gefunden und Weichen gestellt werden. Diese
          Lösungen müssen vor Ort verhandelt und geplant werden. Der Start ist eine fundierte Wärmeplanung. Zwei Punkte
          sind hierbei wichtig:
          <ul className="pt-2">
            <li>Qualitätsanspruch: Die Wärmeplanung muss dem Stand von Wissenschaft und Technik entsprechen.</li>
            <li>
              Ambitionsniveau: Mit Hilfe der Wärmeplanung die Dekarbonisierung der Wärmeversorgung bis 2035
              abgeschlossen sein.
            </li>
          </ul>
          Dafür stellt LocalZero die folgende Checkliste zur Verfügung.
        </div>
        <Accordion
          id="accordionFlushKAP"
          className="accordion-flush pb-3"
        >
          <h5>1. Beschluss zur Durchführung</h5>
          <p>Kommunaler Beschluss zur Durchführung der Wärmeplanung inkl. öffentlicher Bekanntmachung</p>
          <ChecklistItem
            key={0}
            checklist_item={city.energy_plan_checklist[0]}
          />
          <ChecklistItem
            key={1}
            checklist_item={city.energy_plan_checklist[1]}
          />
          <h5 className="pt-4">2. Eignungsprüfung und verkürztes Verfahren (§ 14 WPG)</h5>
          <p>
            Frühzeitiges Ausschlussverfahren: Ausschluss von nicht geeigneten Quartieren/Gebieten für Wärmenetz oder
            Wasserstoffnetz (z.B. für ländliche, zersiedelte Räume)
          </p>
          <ChecklistItem
            key={2}
            checklist_item={city.energy_plan_checklist[2]}
          />
          <ChecklistItem
            key={3}
            checklist_item={city.energy_plan_checklist[3]}
          />
          <h5 className="pt-4">3. Bestandsaufnahme inkl. Wärmebedarfe Status quo (§ 15 WPG)</h5>
          <p>Aktuelle Wärmeversorgung und Wärmebedarf feststellen.</p>
          <ChecklistItem
            key={4}
            checklist_item={city.energy_plan_checklist[4]}
          />
          <ChecklistItem
            key={5}
            checklist_item={city.energy_plan_checklist[5]}
          />
          <h5 className="pt-4">4. Erstellung der Potenzialberechnungen (§ 16 WPG)</h5>
          <p>
            Ziel ist die Ausweisung von Wärmebedarf und Wärmeversorgung im Ist-Zustand und Ziel-Zustand, in Abstimmung
            mit jeweiligen Szenarien. Hier sind zwei unterschiedliche Aspekte entscheidend:
            <br />
            (1) Identifizierung der Potenziale zur erneuerbaren Wärmeerzeugung
            <br />
            (2) Einschätzung über Potenziale zur Energieeinsparung sowie -effizienz durch Wärmebedarfsreduktion in
            Gebäuden sowie in industriellen oder gewerblichen Prozessen
          </p>
          <ChecklistItem
            key={6}
            checklist_item={city.energy_plan_checklist[6]}
          />
          <ChecklistItem
            key={7}
            checklist_item={city.energy_plan_checklist[7]}
          />
          <ChecklistItem
            key={8}
            checklist_item={city.energy_plan_checklist[8]}
          />
          <h5 className="pt-4">5. Erstellung der Zielszenarien (§ 17 WPG)</h5>
          <div>
            <ul>
              <li>Entwicklung des zukünftigen Wärmebedarfs</li>
              <li>Flächenhafte Darstellung zur klimaneutralen Bedarfsdeckung mit jeweiligen Zwischenschritten</li>
            </ul>
          </div>
          <ChecklistItem
            key={9}
            checklist_item={city.energy_plan_checklist[9]}
          />
          <ChecklistItem
            key={10}
            checklist_item={city.energy_plan_checklist[10]}
          />
          <ChecklistItem
            key={11}
            checklist_item={city.energy_plan_checklist[11]}
          />
          <ChecklistItem
            key={12}
            checklist_item={city.energy_plan_checklist[12]}
          />
          <ChecklistItem
            key={13}
            checklist_item={city.energy_plan_checklist[13]}
          />
          <h5 className="pt-4">6. Einteilung in Wärmeversorgungsgebiete und -arten (§18 und 19 WPG)</h5>
          <p>
            Bei der Einteilung in Wärmeversorgungsgebiete passieren zwei Dinge:
            <br />
            (1) Einteilung in voraussichtliche Wärmeversorgungsgebiete und -arten
            <br />
            (2) Darstellung der Wärmeversorgungsarten für das Zieljahr
            <br />
            Aufteilung nach Wärmeversorgungsgebieten (Wärmenetz, Wasserstoff, dezentrale Gebiete), eingeteilt in wo
            welcher Gebietstyp (sehr) (un)wahrscheinlich bzw. (un)geeignet ist. Aufteilung muss in Einklang mit
            vorliegendem/sich in der Erstellung befindlichen Wärmenetzbau- und -dekarbonisierungsfahrplan (Paragraph 32)
            sein
          </p>
          <ChecklistItem
            key={14}
            checklist_item={city.energy_plan_checklist[14]}
          />
          <ChecklistItem
            key={15}
            checklist_item={city.energy_plan_checklist[15]}
          />
          <ChecklistItem
            key={16}
            checklist_item={city.energy_plan_checklist[16]}
          />
          <h5 className="pt-4">7. Umsetzungsstrategie und konkrete Umsetzungsmaßnahmen (§ 20 WPG)</h5>
          <p>
            Ziel muss ein ambitionierter Transformationspfad mit klaren Maßnahmen und jahresscharfer Planung mit
            schnellstmöglichem Start sein. Die Kommune („planungsverantwortliche Stelle“) muss im Rahmen ihrer
            Möglichkeiten selbst Maßnahmen durchführen, mit denen das Zielszenario erreicht werden kann, oder Dritte
            dazu beauftragen. Die Wärmeplanung ist eine Strategie, nicht einfach nur Daten und Fakten. Daher ist es
            wichtig, dass alle Akteure (s.u.) klare Rollen und Aufgaben haben und diese ineinandergreifen.
          </p>
          <ChecklistItem
            key={17}
            checklist_item={city.energy_plan_checklist[17]}
          />
          <ChecklistItem
            key={18}
            checklist_item={city.energy_plan_checklist[18]}
          />
        </Accordion>
      </Container>
    </>
  );
}
