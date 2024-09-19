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
                <a href="https://localzero.net/" target="new">LOCALZERO</a>
              </li>
              <li>
                {" "}
                <a href="/datenschutz">DATENSCHUTZ</a>
              </li>
              <li>
                {" "}
                <a href="/impressum">IMPRESSUM</a>
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
              link="https://www.linkedin.com/showcase/localzero/"
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
                src="/imgs/itz_weiss_transp.png"
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
                GermanZero e.V.
              </a>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
