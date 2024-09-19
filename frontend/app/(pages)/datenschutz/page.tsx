import { Container } from "react-bootstrap";

export const dynamic = 'force-static';
export default async function ProjectDescription() {


  return (
    <Container className="py-3 w-75 m-auto">

        <h1 className="big-h1">Datenschutz</h1>
        <p>
    LocalZero gehört zum&nbsp;<a href="https://www.germanzero.de/" rel="noopener noreferrer nofollow">GermanZero e.V.</a>
  </p>
  <h3>Datenschutzerklärung</h3>
  <p>
    Es gelten die Datenschutzbestimmungen gemäß <a href="https://www.germanzero.de/datenschutz" target="_blank">https://www.germanzero.de/datenschutz</a>.
  </p>


    </Container>
  );
}
