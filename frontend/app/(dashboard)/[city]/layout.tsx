import { getCities } from "@/lib/dataService";
import { City } from "@/types";
import "bootstrap/dist/css/bootstrap.min.css";
import Header from "@/app/components/Header";
import Footer from "@/app/components/Footer";
import BreadCrumb from "@/app/components/BreadCrumb";
import { Container } from "react-bootstrap";



export default async function DashboardLayout({
  children,
  params
}: Readonly<{
  children: React.ReactNode;
  params: { city: string }
}>) {
  const city:City = await getCities(params.city);
  return (
    <Container>
        <Header />
        <BreadCrumb logo={city.local_group?.logo} cityName={city.name}></BreadCrumb>
        {children}
        <Footer />
    </Container>
  );
}
