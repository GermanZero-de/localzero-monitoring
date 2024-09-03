export async function getCities(id: string = "") {
  const slug = id ? `/${id}` : ""
  try {
    const cities = await (await fetch(`${process.env.REST_API}/api/cities${slug}`, {
      cache: "no-store",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
      },
    })).json();
    return cities
  } catch (e) {
    console.error(e)
    return []
  }
}

export async function getTasks(id: string = "") {
  const slug = id ? `/${id}` : ""
  try {
    const tasks = await (await fetch(`${process.env.REST_API}/api/cities${slug}/tasks`, {
      cache: "no-store",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
      },
    })).json();
    return tasks
  } catch (e) {
    console.error(e)
    return []
  }
}