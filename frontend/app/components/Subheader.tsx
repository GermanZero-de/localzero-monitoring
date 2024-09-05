import banner from "@/public/imgs/dashboard-banner.jpg";
import Image from "next/image";
import styles from "./styles/Subheader.module.scss";
import { Container } from "react-bootstrap";
export default function Subheader() {
  return (
    <Container>
    <div className={styles.banner}>
    <h1 className={styles.textPrimary}>Auf dem Weg zur Klimaneutralität</h1>
    <h1 className={styles.textSecondary}>Klimaschutz-Monitoring von Kommunen</h1>

    <Image
      unoptimized
      fill
      style={{ objectFit: "cover" }}
      src="/images/background.webp"
      alt="Fröhliches Kind mit Strohhut in einer grünen Stadt"
    />
  </div>
  </Container>
  );
}
