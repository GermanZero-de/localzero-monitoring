import Image from "next/image";
import styles from "./styles/Subheader.module.scss";
import { Container } from "react-bootstrap";
import heroimage from "@/public/hero-image.webp";
export default function Subheader() {
  return (
    <Container>
    <div className={styles.banner}>
    <span
      className={styles.textPrimary}
    >
      Auf dem Weg zur Klimaneutralität
    </span>

    <Image
      unoptimized
      fill
      style={{ objectFit: "cover", objectPosition:"70%", boxShadow: "0 10px 10px -5px rgba(0,0,0,.15)" }}
      src={heroimage}
      alt="Begrünter Stadtplatz mit vielen Bäumen"
    />
  </div>
  </Container>
  );
}
