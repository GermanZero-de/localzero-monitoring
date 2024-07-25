import { getCities } from "@/lib/dataService";
import { City } from "@/types";
import { Container } from "react-bootstrap";


export default async function Home() {
  const all_cities = await getCities();
  return (
    <Container className="min-vh-50 p-3">
      <ul className="list-none">
        {all_cities?.map((city:City) => (
          <li
            key={city.id}
            className="list-item"
          >
            <h2 className="headingWithBar">{city.name}</h2>
            <p className="text-base">{city.teaser}</p>
          </li>
        ))}
      </ul>
    </Container>
  );
}
