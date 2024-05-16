"use client";
import { Container, Navbar, Nav, NavDropdown } from "react-bootstrap";

export default function Header() {
  return (
    <Navbar
      color="light"
      expand="lg"
      className="border-bottom border-gray bg-white"
      style={{ height: 80 }}
    >
      <Container>
        <Navbar.Brand href="/">
          {" "}
          <img
            src="/logo.png"
            width="200px"
            className="d-inline-block align-top"
            alt="LocalZero Monitoring logo"
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="m-auto fw-bold">
            <NavDropdown title="TOP-MASSNAHMEN">
              <NavDropdown.Item href="start">START</NavDropdown.Item>
              <NavDropdown.Item href="projektbeschreibung">
                PROJEKTBESCHREIBUNG
              </NavDropdown.Item>
              <NavDropdown.Item href="mitmachen">MITMACHEN</NavDropdown.Item>
              <NavDropdown.Item href="kontakt">KONTAKT</NavDropdown.Item>
              <NavDropdown.Item href="impressum">IMPRESSUM</NavDropdown.Item>
              <NavDropdown.Item href="datenschutz">
                DATENSCHUTZ
              </NavDropdown.Item>
            </NavDropdown>

            <Nav.Link href="#suche_kommune">SUCHE KOMMUNE</Nav.Link>
            <NavDropdown title="TOP-MASSNAHMEN" id="basic-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">
                Another action
              </NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action/3.4">
                Separated link
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
        <Navbar.Brand href="#home">
          <img
            src="/spende.svg"
            width="200px"
            className="d-inline-block align-top"
            alt="Spenden"
          />
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
}
