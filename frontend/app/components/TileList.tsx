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
    <div className="d-flex justify-content-start flex-wrap">
     {visibleCities.map((city:City) => (
            <Link
              key={city.slug}
              href={"/" + city.slug}
              style={{color:"black", textDecoration:"none"}}
            >
              <Tile
                name={city.name}
                logo={city.local_group?.logo}
              />
            </Link>
          ))}
    </div>
    <div className="block-text pb-3">
          {!showAll ? <div>Anzeige weiterer Kommunen</div> : <></>}
          <Image
            onClick={toggle}
            src={showAll ? expandArrowUp : expandArrowDown}
            alt="Anzeige weiterer Kommunen"
            style={{cursor:"pointer"}}
          />
        </div>
    </div>

  );
};

export default TileList;