import axios from "axios";
import { useState, useEffect } from "react";

interface LocalGroup {
  id: number;
  name: string;
  website: string;
  teaser: string;
  description: string;
  logo: string;
  featured_image: string;
}

interface ChecklistItem {
  id: number;
  question: string;
  is_checked: boolean;
  help_text: string;
  rationale: string;
}

export interface CityData {
  id: number;
  name: string;
  municipality_key: string;
  url: string;
  resolution_date: string;
  target_year: number;
  teaser: string;
  description: string;
  assessment_status: string;
  contact_name: string;
  contact_email: string;
  supporting_ngos: string;
  slug: string;
  local_group: LocalGroup;
  cap_checklist: ChecklistItem[];
  administration_checklist: ChecklistItem[];
  assessment_action_plan: string;
  assessment_administration: string;
}

export function useGetCity(slug: string): {
  city: CityData | undefined;
  hasError: boolean;
} {
  const [city, setCity] = useState<CityData | undefined>(undefined);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    const getCity = async () => {
      const response = await axios
        .get("http://127.0.0.1:8000/api/cities/" + slug, {
          // TODO: proper url
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json;charset=UTF-8",
          },
        })
        .then((response) => {
          setCity(response.data);
        })
        .catch((error) => {
          setHasError(true);
          console.error("Error get city request: ", error);
        });
    };

    getCity();
  }, [slug]);

  return { city, hasError };
}
