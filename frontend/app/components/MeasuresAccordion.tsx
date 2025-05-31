"use client";

import { Accordion } from "react-bootstrap";
import MeasureCard from "@/app/components/MeasureCard";
import MeasureCardContent from "@/app/components/MeasureCardContent";
import { getRecursiveStatusNumbers } from "@/lib/utils";
import styles from "./MeasuresAccordion.module.scss";
import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";

interface MeasuresAccordionProps {
  tasks: any[];
}

export default function MeasuresAccordion({ tasks }: MeasuresAccordionProps) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [activeKey, setActiveKey] = useState<string>("");

  useEffect(() => {
    const active = searchParams.get("active");
    if (active) {
      setActiveKey(active);
    }
  }, [searchParams]);

  const handleSelect = (key: string | null) => {
    const newKey = key || "";
    setActiveKey(newKey);

    const params = new URLSearchParams(searchParams.toString());

    if (newKey) {
      params.delete("activesub");
      params.set("active", newKey);
    } else {
      params.delete("active");
      params.delete("activesub");
    }
   
    router.replace(`?${params.toString()}`, { scroll: false });
  };

  return (
    <Accordion
      className={styles.accordion}
      activeKey={activeKey}
      onSelect={(key) => handleSelect(key as string)}
    >
      {tasks &&
        tasks.map((task: any, i: number) => {
          return (
            <MeasureCard
              key={i}
              eventKey={task.slugs.split("/")[0]}
              title={task.title}
              statusOfSubTasks={getRecursiveStatusNumbers(task.children)}
            >
              <MeasureCardContent
                activeKey={activeKey}
                slugs={task.slugs}
                text={task.teaser}
                tasks={task.children}
                eventKey={task.slugs}
              ></MeasureCardContent>
            </MeasureCard>
          );
        })}
    </Accordion>
  );
}