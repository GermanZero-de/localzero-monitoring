import { db } from "../db/db.server";
import { cpmonitorCity } from "../db/schema";
import { Container } from "react-bootstrap";

async function getCities() {
  const cities = await db.select().from(cpmonitorCity)
  return cities;
}


export default async function Home() {
  const all_cities = await getCities();
  return (
    <Container className="p-3 min-vh-50">
     <ul className="list-none">
        {all_cities?.map((city) => (
            <li key={city.id} className="list-item">
              <h2 className="text-xl font-semibold">{city.name}</h2>
              <p className="text-base">{city.teaser}</p>
            </li>
          ))}
      </ul>
     </Container>
  );
}
