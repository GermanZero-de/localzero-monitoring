"use client";

import React, { useEffect, useState } from "react";
import { Accordion } from "react-bootstrap";
import styles from "./styles/MeasureCard.module.scss";
import LinkMeasureCard from "./LinkMeasureCard";
import SecondaryMeasureCard from "./SecondaryMeasureCard";
import { Task } from "@/types";
import { useRouter, useSearchParams } from "next/navigation";

interface MeasureCardContentProps {
  text: string;
  tasks: Task[];
  eventKey: string;
  slugs: string;
  activeKey: string;
}

const MeasureCardContent: React.FC<MeasureCardContentProps> = ({ text, tasks, slugs, eventKey}) => {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [activeKey, setActiveKey] = useState<string>("");

  useEffect(() => {
    const active = searchParams.get(eventKey.substring(0,5));
    const matchingChildTask = tasks.find((t) => t.slugs.split("/").pop() === active);

    if (matchingChildTask) {
      setActiveKey(matchingChildTask.slugs);
    }
  }, [searchParams]);

  const handleSelect = (key: string | null) => {
    const newKey = key || "";
    const lastSegment = newKey.split("/").pop()!;
    const params = new URLSearchParams(searchParams.toString());
    const keyPart = eventKey.substring(0,5);

    setActiveKey(newKey);
  
    if (newKey) {
      params.set(keyPart, lastSegment);
    } else {
      params.delete(keyPart);
    }
  
    router.replace(`?${params.toString()}`, { scroll: false });
  };  

  return (
    <div >
      {text} <a href={"./massnahmen/"+slugs}>Mehr lesen...</a>
      <Accordion className={styles.contentaccordion} activeKey={activeKey} onSelect={(key) => handleSelect(key as string)}>
        {tasks.map((task, i) => {
          if (task.numchild && task.children.length > 0) {
            return (
              <SecondaryMeasureCard
                eventKey={task.slugs}
                key={i}
                title={task.title}
                source={task.source}
              >
                <MeasureCardContent
                  activeKey={activeKey}
                  slugs={task.slugs}
                  text={task.teaser}
                  tasks={task.children}
                  eventKey={`p${eventKey}c${i}`}
                ></MeasureCardContent>
              </SecondaryMeasureCard>
            );
          } else {
            return (
              <LinkMeasureCard
                slugs={task.slugs}
                title={task.title}
                taskStatus={task.execution_status}
                key={i}
                source={task.source}
              ></LinkMeasureCard>
            );
          }
        })}
      </Accordion>
    </div>
  );
};

export default MeasureCardContent;
