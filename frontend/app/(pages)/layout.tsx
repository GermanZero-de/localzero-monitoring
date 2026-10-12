import { getCities } from "@/lib/dataService";
import { City } from "@/types";
import Header from "@/app/components/Header";
import Footer from "@/app/components/Footer";
import Subfooter from "@/app/components/Subfooter";
import { Container } from "react-bootstrap";

// @next-codemod-ignore Cache Components adoption: this segment temporarily allows blocking.
// Remove this opt-out after verifying the segment passes validation without it.
// See: https://nextjs.org/docs/app/guides/migrating-to-cache-components
export const instant = false;

export default async function PagesLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cities: City[] = await getCities();
  return (
    <Container>
      <Header />

      {children}
      <Subfooter cities={cities} />
      <Footer />
    </Container>
  );
}
