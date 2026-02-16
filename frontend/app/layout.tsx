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
    // TODO: inject the ID once we created it, via environment variable
    <Script
        defer
        src="https://analytics.monitoring.localzero.net/script.js"
        data-website-id="5d6b2df8-64ad-4a58-b4f1-b765d99ba9b1"
        />
      </body>
    </html>
  );
}
