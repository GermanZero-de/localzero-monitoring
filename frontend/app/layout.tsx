import type { Metadata } from "next";
import Script from 'next/script'
import { Inter } from "next/font/google";
import { getCities } from "@/lib/dataService";
import { City } from "@/types";
import "bootstrap/dist/css/bootstrap.min.css";
import "./globals.scss";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "LocalZero Monitoring",
  description: "Monitoring von Klimaschutz-Maßnahmen in LocalZero-Kommunen",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cities:City[] = await getCities();
  return (
    <html lang="de">
      <head>
        <link
          rel="icon"
          href="/favicon.svg"
          sizes="any"
        />
      </head>
      <body className={inter.className}>
        {children}
    <Script
        defer
        src="/umami/script.js"
        data-website-id="b718ea63-70a1-4ab8-8391-089fb1336a41"
        />
      </body>
    </html>
  );
}
