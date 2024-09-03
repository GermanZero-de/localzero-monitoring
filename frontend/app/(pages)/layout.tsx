import { getCities } from "@/lib/dataService";
import { City } from "@/types";
import Header from "@/app/components/Header";
import Subheader from "@/app/components/Subheader";
import Footer from "@/app/components/Footer";
import Subfooter from "@/app/components/Subfooter";
import { Container } from "react-bootstrap";

export default async function PagesLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cities: City[] = await getCities();
  return (
    <Container>
      <Header />
      <Subheader />
      {children}
      <Subfooter cities={cities} />
      <Footer />
    </Container>
  );
}
