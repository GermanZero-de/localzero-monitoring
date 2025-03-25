import {cookies} from 'next/headers';


const getCookie = async (name: string) => {
  return cookies().get(name)?.value ?? '';
}

export async function getCities(id: string = "") {
  const sessionid = await getCookie('sessionid');
  const revalidate = sessionid ? 0: 1800;
  const slug = id ? `/${id}` : ""
    const cities = await (await fetch(`${process.env.REST_API || "http://localhost:8000"}/api/cities${slug}?executionStatusCount`, {
      next: { revalidate },
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        Cookie: `sessionid=${sessionid};`
      },
    })).json();
    return cities

}

export async function getTasks(id: string = "") {
  const slug = id ? `/${id}` : ""
  const sessionid = await getCookie('sessionid');
  const revalidate = sessionid ? 0: 1800;
    const tasks = await (await fetch(`${process.env.REST_API || "http://localhost:8000"}/api/cities${slug}/tasks`, {
      next: { revalidate },
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
         Cookie: `sessionid=${sessionid};`
      },
    })).json();
    return tasks

}

