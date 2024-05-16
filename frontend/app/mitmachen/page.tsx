import Image from "next/image";
import styles from "./page.module.scss";
import { Container } from "react-bootstrap";
import Card from "../components/Card";
export default function Home() {
  return (
    <Container className="p-3">
      <Card title={"Ein titel"}> </Card>
      <Card title={"Ein anderer titel"}> </Card>
    </Container>
  );
}
