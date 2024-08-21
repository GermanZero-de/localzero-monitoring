export async function getCities(id:string = "") {
    const slug = id ? `/${id}` : ""
    const cities = await (await fetch(`${process.env.REST_API}/api/cities${slug}`, {
        cache:"no-store",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json;charset=UTF-8",
        },
      })).json();
      return cities
}