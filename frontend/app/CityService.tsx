import axios from "axios";
import { useState, useEffect } from "react";

export function useGetCity(slug: string | undefined) {
  const [city, setCity] = useState(undefined);
  const [hasError, setHasError] = useState(false);

  if (!slug) {
    setHasError(true);
    return { undefined, hasError };
  }

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

  useEffect(() => {
    getCity();
  }, []);

  return { city, hasError };
}
