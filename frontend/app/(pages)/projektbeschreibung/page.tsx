import { Container } from "react-bootstrap";

export default async function ProjectDescription() {


  return (
    <Container>
      <div className="py-3 w-50 m-auto">
        <h1 className="big-h1">DAS PROJEKT</h1>

        In vielen Kommunen geraten die Bemühungen um Klimaneutralität früher oder später ins Stocken. Kein Wunder, denn
        es gibt bundesweit keine Blaupause dafür, wie dieses Ziel zu erreichen ist. Die Kommunen und ihre Bürger:innen
        begehen hier permanent Neuland und stoßen auf zahlreiche Fragen und Hindernisse. Für Bürger:innen ist häufig
        nicht ersichtlich, ob ihre Kommune überhaupt Fortschritte erzielt.
      </div>
      <h1 className="headingWithBar w-75 m-auto">Kommunen im Monitoring</h1>
      <div className="py-3 w-50 m-auto">
        <p>
          Deshalb hat LocalZero die Plattform LocalMonitoring ins Leben gerufen. LocalMonitoring macht Fortschritte
          sichtbar, damit sie gefeiert werden können – und es zeigt Hürden auf, damit sie beseitigt werden können.
        </p>


        <h4 className="pt-2">Im Fokus der Bewertung stehen drei Aspekte:</h4>
        <ul>
          <li>Der Klima-Aktionsplan einer Kommune</li>
          <li>Die Verwaltungsstruktur der Kommune</li>
          <li>Die Umsetzungsstände von beschlossenen Klimaschutzmaßnahmen</li>
        </ul>
        <h4 className="pt-2">LocalMonitoring bietet Übersicht und Transparenz</h4>
        Als öffentlich zugängliche Plattform hilft LocalMonitoring der Verwaltung und stärkt die Akzeptanz bei den
        Bürger:innen, indem es
        <ul>
          <li>die wichtigsten Maßnahmen auf dem Weg zur Klimaneutralität aufzeigt</li>
          <li>Struktur in ein komplexes Thema bringt</li>
          <li>die Debatte um die richtigen Klimaschutzmaßnahmen versachlicht.</li>
          <li>
            als konstruktive Grundlage für den Austausch mit anderen Organisationen und Stakeholdern wie z. B.
            ansässigen Wirtschaftsunternehmen oder Umweltverbänden dient.
          </li>
        </ul>
        <h4 className="pt-2">LocalMonitoring unterstützt Kommunen bei der Umsetzung</h4>
        Unterstützt von den beteiligten Teams kann eine Stadt zeigen, wo es Erfolge und Anstrengungen gibt.
        <ul>
          <li>
            Belastbare Zahlen und Fakten ermöglichen den konstruktiven Dialog mit der Zivilgesellschaft. Gemeinsam
            werden Flaschenhälse und Hemmnisse identifiziert.
          </li>
          <li>
            Die Plattform hilft dabei, objektiv zu zeigen, wo der Einfluss der Kommune endet und das Land oder der Bund
            helfen muss.
          </li>
          <li>LocalMonitoring basiert auf der ehrenamtlichen Arbeit von Teams vor Ort.</li>
          <li>Erarbeitet und gepflegt wird das Monitoring einer Stadt stets von einem Team vor Ort.</li>
          <li>Die ehrenamtlichen Teams werden unterstützt von der LocalZero-Zentrale und den anderen Teams.</li>
          <li>
            Die Teams pflegen gute Kontakte zur Kommunalpolitik und der Verwaltung und befinden sich im konstruktiven
            Dialog mit diesen.
          </li>
        </ul>
      </div>
      <h1 className="headingWithBar  w-75 m-auto">Über uns</h1>
      <div className="py-3 w-50 m-auto">
        <h4>LocalMonitoring wird ehrenamtlich von engagierten Bürger:innen der jeweiligen Stadt betrieben.</h4>
        LocalMonitoring ist ein Projekt der Initiative LocalZero, dem Netzwerk für kommunale Klimaneutralität unter dem
        Dach von{" "}
        <a
          href="https://germanzero.de/"
          target="_blank"
        >
          GermanZero
        </a>
        . Teams von LocalZero sind in mehr als 90 Städten in Deutschland aktiv. In über 40 Städten haben sie bereits
        Beschlüsse für Klimaneutralität bis spätestens 2035 bewirkt.
        <h4 className="pt-2">Mehr zu LocalZero</h4>
        Weil es bundesweit keine Blaupausen für die komplexen Schritte gibt, die eine Kommune unternehmen muss, um
        klimaneutral zu werden, hat sich LocalZero zum Ziel gesetzt, die Kommunen und ihre engagierten Bürger:innen mit
        Knowhow und Best Practices zu unterstützen.
        <div className="pt-2">
          <b>Wichtige Instrumente hierfür sind</b>
        </div>
        <ul>
          <li>
            Die Klimavision – eine für jede Kommune in 30 Sekunden erstellbare erste Übersicht über den Umfang der
            nötigen Maßnahmen, inklusive überschlägiger Energie- und Treibhausbilanz.
          </li>
          <li>
            Klimaentscheide – mit den Mitteln direkter Demokratie organisieren Bürger:innen Mehrheiten. Das Ziel: Ihre
            Stadt oder Gemeinde beschließt, einen Klimaschutzplans zu erstellen, mit dem sie bis spätestens 2035
            klimaneutral werden kann.
          </li>
          <li>
            Beratung zu Klimaaktionsplänen (KAP) – KAPs geben detailliert an, mit welchen Schritten, eine Kommune
            klimaneutral werden kann. Viele KAP sind jedoch unkonkret bei Zeitplanung, Zielbeschreibung und
            Maßnahmenauswahl. Wir zeigen, wie es besser geht.
          </li>
          <li>
            LocalMonitoring – die Plattform für das Monitoring von beschlossenen und gegebenenfalls zusätzlich nötigen
            Klimaschutzmaßnahmen.
          </li>
        </ul>
      </div>
    </Container>
  );
}
