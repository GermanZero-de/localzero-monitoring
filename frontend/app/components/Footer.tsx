import { Container, Row, Col } from "react-bootstrap";
import SocialIcon from "./SocialIcon";
import styles from "./styles/Footer.module.scss";
export default function Footer() {
  return (
    <div className="bg-secondary mt-auto">
      <Container className="p-3">
        <Row>
          <Col className="content-align-left fs-5 text-left text-white">
            <ul className="footer-nav-list">
              <li>
                {" "}
                <a href="/start">DAS PROJEKT</a>
              </li>
              <li>
                {" "}
                <a href="/komunen">KOMMUNEN</a>
              </li>
              <li>
                {" "}
                <a href="topmassnahmen">TOP-MASSNAHMEN</a>
              </li>
              <li>
                {" "}
                <a href="https://germanzero.de/">LOKALZERO</a>
              </li>
            </ul>
          </Col>
          <Col className="d-flex align-items-center text-center">
            <SocialIcon
              name="facebook"
              link="https://de-de.facebook.com/GermanZero.NGO"
            />
            <SocialIcon
              name="x"
              link="https://twitter.com/_germanzero"
            />
            <SocialIcon
              name="youtube"
              link="https://www.youtube.com/channel/UCyio7GV0kpXeOu5m6Xo6A3A"
            />
            <SocialIcon
              name="linkedin"
              link="https://www.linkedin.com/company/germanzero/"
            />
            <SocialIcon
              name="instagram"
              link="https://www.instagram.com/_GermanZero/"
            />
          </Col>
          <Col className="d-flex align-items-center justify-content-end text-center">
            <a
              href="https://www.transparency.de/"
              rel="noopener nofollow"
              target="_blank"
            >
              <img
                alt=""
                height={50}
                src="/images/itz_weiss_transp.png"
              />
            </a>
          </Col>
        </Row>
        <Row>
          <Col className={[styles.text, "text-center text-white"].join(" ")}>
            <div className="align-items-top col d-flex footer-subline justify-content-center mt-3">
              <div>LocalZero ist ein Teil von&nbsp;</div>{" "}
              <a
                className="link-underline-light link-light"
                href="https://germanzero.de/"
                target="_blank"
              >
                {" "}
                Germanzero e.V.
              </a>
            </div>

            <div className="align-items-top col d-flex footer-subline justify-content-center mt-3">
              <div>🌱 </div>{" "}
              <div>
                {" "}
                Gebaut mit{" "}
                <a
                  className="link-underline-light link-light"
                  href="https://getkirby.com/"
                  target="_blank"
                >
                  Kirby
                </a>
                , gehostet mit 100% erneuerbarer Energie in der Schweiz durch{" "}
                <a
                  className="link-underline-light link-light"
                  href="https://datacenterlight.ch/"
                  target="_blank"
                >
                  ungleich glarus ag
                </a>{" "}
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
