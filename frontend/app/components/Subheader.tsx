import Image from "next/image";
import styles from "./styles/Subheader.module.scss";
import { Container } from "react-bootstrap";
export default function Subheader() {
  return (
    <Container>
    <div className={styles.banner}>
    <span className={styles.textPrimary}>Auf dem Weg zur Klimaneutralität</span>

    <Image
      unoptimized
      fill
      style={{ objectFit: "cover", objectPosition:"70%" }}
      src="/images/background.webp"
      alt="Fröhliches Kind mit Strohhut in einer grünen Stadt"
    />
  </div>
  </Container>
  );
}
