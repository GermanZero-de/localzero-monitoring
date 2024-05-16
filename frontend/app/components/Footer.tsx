import { Container, Row, Col } from "react-bootstrap";
import SocialIcon from "./SocialIcon";
export default function Footer() {
  return (
    <div className="bg-secondary mt-auto">
      <Container className="p-3">
        <Row>
          <Col className="text-left content-align-left text-white fs-5">
            <ul className="footer-nav-list">
              <li> <a href="/start">DAS PROJEKT</a></li>
              <li> <a href="/komunen">KOMMUNEN</a></li>
              <li> <a href="topmassnahmen">TOP-MASSNAHMEN</a></li>
              <li> <a href="https://germanzero.de/">LOKALZERO</a></li>

            </ul>

          </Col>
          <Col className="text-center d-flex">
              <SocialIcon name="facebook" link="https://de-de.facebook.com/GermanZero.NGO"/>
              <SocialIcon name="x" link="https://twitter.com/_germanzero"/>
              <SocialIcon name="youtube" link="https://www.youtube.com/channel/UCyio7GV0kpXeOu5m6Xo6A3A" />
              <SocialIcon name="linkedin" link="https://www.linkedin.com/company/germanzero/"/>
              <SocialIcon name="instagram" link="https://www.instagram.com/_GermanZero/"/>
           </Col>
          <Col className="text-center">
            <a href="/">logo</a>
          </Col>
        </Row>
        <Row>
          <Col className="text-center text-white">
            Gebaut mit Kirby, gehostet mit 100% erneuerbarer Energie in der Schweiz durch ungleich glarus ag
          </Col>

        </Row>
      </Container>
    </div>
  );
}
