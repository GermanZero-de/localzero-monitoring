import Image from "next/image";
import styles from "./styles/Subheader.module.scss";
import { Container } from "react-bootstrap";
import heroimage from "@/public/hero-image.webp";
export default function Subheader() {
  return (
    <Container>
    <div className={styles.banner}>
    <span className={styles.textPrimary}>Auf dem Weg zur Klimaneutralität</span>

    <Image
      unoptimized
      fill
      style={{ objectFit: "cover", objectPosition:"70%" }}
      src={heroimage}
      alt="Begrünter Stadtplatz mit vielen Bäumen"
    />
  </div>
  </Container>
  );
}
