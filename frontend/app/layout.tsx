import type { Metadata } from "next";
import { Inter } from "next/font/google";

import 'bootstrap/dist/css/bootstrap.min.css';
import Header from "./components/Header";
import Footer from "./components/Footer";
import { Container, Row, Col } from 'react-bootstrap';
import "./globals.scss";
const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "LocalZero Monitoring",
  description: "Monitoring von Klimaschutz-Maßnahmen in LocalZero-Kommunen",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="de">
      <body className={inter.className}>
      <Header />
      <Container>
        {children}

      </Container>
      <Footer />


      </body>
    </html>
  );
}
