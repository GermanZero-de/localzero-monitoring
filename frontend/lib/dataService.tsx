export async function getCities(id: string = "") {
  const slug = id ? `/${id}` : ""

    const cities = await (await fetch(`${process.env.REST_API || "http://localhost:8000"}/api/cities${slug}`, {
      cache: "no-store",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
      },
    })).json();
    return cities

}

export async function getTasks(id: string = "") {
  const slug = id ? `/${id}` : ""

    const tasks = await (await fetch(`${process.env.REST_API || "http://localhost:8000"}/api/cities${slug}/tasks`, {
      cache: "no-store",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
      },
    })).json();
    return tasks

}