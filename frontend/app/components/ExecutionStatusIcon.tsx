import React from "react";
import Image from "next/image";
import { ExecutionStatus } from "@/types/enums";
import abgeschlossen from "@/public/imgs/icon-abgeschlossen.svg";
import gescheitert from "@/public/imgs/icon-gescheitert.svg";
import inArbeit from "@/public/imgs/icon-in_arbeit.svg";
import unbekannt from "@/public/imgs/icon-unbekannt.svg";
import verzoegert from "@/public/imgs/icon-verzoegert_fehlt.svg";
import { executionLabels } from "@/lib/utils";

interface ExecutionStatusIconProps {
  taskStatus: ExecutionStatus;
  disabled?: boolean
}

const ExecutionStatusIcon: React.FC<ExecutionStatusIconProps> = ({ taskStatus, disabled }) => {
  let icon = unbekannt;
  let altText = "";
  switch (taskStatus) {
    case ExecutionStatus.UNKNOWN:
      icon = unbekannt;
      altText = "Maßnahmen mit unbekanntem Status";
      break;
    case ExecutionStatus.AS_PLANNED:
      icon = inArbeit;
      altText = "Maßnahmen in Arbeit";
      break;
    case ExecutionStatus.COMPLETE:
      icon = abgeschlossen;
      altText = "abgeschlosse Maßnahmen";
      break;
    case ExecutionStatus.DELAYED:
      icon = verzoegert;
      altText = "verzögerte Maßnahmen";
      break;
    case ExecutionStatus.FAILED:
      icon = gescheitert;
      altText = "gescheiterte Maßnahmen";
      break;
  }
  const imageStyle = disabled ? { filter: "grayscale(90%) contrast(50%) brightness(120%)" } : {};

  return (
    <Image
      src={icon}
      alt={altText}
      style={imageStyle}
      title={altText}
    ></Image>
  );
};

export default ExecutionStatusIcon;
