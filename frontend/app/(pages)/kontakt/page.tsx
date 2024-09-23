import { Container } from "react-bootstrap";
import Image from "next/image";
import philipp from "@/public/imgs/philipp.webp";
import leonie from "@/public/imgs/leonie.webp";
import highlight_portr from "@/public/imgs/highlight_portr.svg";
import styles from "./page.module.scss";
import arrow from "@/public/imgs/arrow-right-down.svg";
import Link from "next/link";

export default function ProjectDescription() {
  return (
    <Container>

      <div className="py-3 w-sm-50 m-auto">
      <h1 className="big-h1">Kontakt</h1>
        Wir haben uns bemüht die Informationen und die Website sehr klar aufzubereiten, aber es ergeben sich immer Fragen. Darum scheue nicht uns zu kontaktieren ...
      </div>
      <h2 className="headingWithBar w-sm-75 m-auto">Monitoring</h2>
      <p className="py-3 w-sm-50 m-auto d-flex position-relative">
        <p className="flex-grow-1">
          Philipp beantwortet dir alle Fragen zum Monitoring, zur Website... Bitte schicke eine E-Mail oder vereinbare einen Termin
          <Image
          src={arrow}
          alt=""
        />
        </p>
        <Link href="mailto:philipp.nuske@germanzero.de">
          <Image
                src={highlight_portr}
                alt="hightlight"
                className={styles.kontaktPic}
              />
          <Image
                src={philipp}
                alt="Philipp"
              />
          </Link>
      </p>
      <h2 className="headingWithBar w-sm-75 m-auto">Lokalteams</h2>
      <p className="py-3 w-sm-50 m-auto d-flex position-relative">
        <p className="flex-grow-1">
        Leonie beantwortet dir alle Fragen zu den Lokalteams... Bitte schicke eine E-Mail oder vereinbare einen Termin
        <Image
          src={arrow}
          alt=""
        />
        </p>
        <Link href="mailto:Leoni.Rohlfs@GermanZero.de">
        <Image
              src={highlight_portr}
              alt="hightlight"
              className={styles.kontaktPic}
            />
        <Image
              src={leonie}
              alt="Leonie"
            />
       </Link>
      </p>

      <h2 className="headingWithBar w-sm-75 m-auto">Maßnahmen</h2>
      <div className="py-3 w-sm-50 m-auto">
      Johannes beantwortet dir alle Fragen zu den Maßnahmen... Bitte schicke eine E-Mail oder vereinbare einen Termin
      </div>
    </Container>
  );
}
