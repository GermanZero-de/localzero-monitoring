"use client"

import { useState } from "react";
import type {City} from "@/types"
import Link from "next/link";
import Tile from "./Tile";
import Image from "next/image";
import expandArrowUp from "@/public/imgs/arrow-expand-up.svg";
import expandArrowDown from "@/public/imgs/arrow-expand-down.svg";

interface TileListProps {
    cities: City[];
  }

  const TileList: React.FC<TileListProps> = ({ cities }) => {

    const [showAll, setShowAll] = useState(false);


    const toggle = () => {
      setShowAll((prevShowAll) => !prevShowAll);
    };



    // Determine how many divs to display based on state
    const visibleCities = showAll ? cities : cities.slice(0, 4);

    return (
      <div>
      <div className="d-flex justify-content-start flex-wrap" style={{gap:"24px"}}>
      {visibleCities.map((city:City) => (
              <Link
                key={city.slug}
                href={"/" + city.slug}
                style={{color:"black", textDecoration:"none"}}
                data-testid="city-tile"
              >
                <Tile
                  name={city.name}
                  logo={city.local_group?.logo_square}
                  executionStatus={city?.executionStatusCount}
                  startYear={city.resolution_date ? new Date(city.resolution_date).getFullYear() : null}
                  endYear={city.target_year}
                />
              </Link>
            ))}
      </div>
      <div className="block-text pb-3" onClick={toggle} style={{cursor:"pointer"}}>
            <div className="lh-4 py-4">{!showAll ? "weitere Kommunen" : "weniger"}</div>
            <Image
              src={showAll ? expandArrowUp : expandArrowDown}
              alt="weitere Kommunen"
            />
          </div>
      </div>

    );
  };

export default TileList;