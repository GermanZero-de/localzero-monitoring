import { getCities, getTasks } from "@/lib/dataService";
import { City, Task } from "@/types";
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
  const tasks:Task[] = await getTasks(params.city);

  return (
    <Container>
        <Header />
        <BreadCrumb logo={city.local_group?.logo} tasks={tasks} cityName={city.name}></BreadCrumb>
        {children}
        <Footer />
    </Container>
  );
}
