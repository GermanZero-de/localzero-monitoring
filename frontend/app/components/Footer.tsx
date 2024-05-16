import { Container, Row, Col } from "react-bootstrap";

export default function Footer() {
  return (
    <div className="bg-secondary mt-auto">
      <Container className="p-3">
        <p className="text-center text-white">Thank you for visiting this website</p>
        <p className="mt-5 text-center text-white">Follow us on social media:</p>
        <Row>
          <Col className="text-center">
            <a href="/">Instagram</a>
          </Col>
          <Col className="text-center">
            <a href="/">Facebook</a>
          </Col>
          <Col className="text-center">
            <a href="/">Twitter</a>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
