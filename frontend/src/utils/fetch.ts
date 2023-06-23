export const API_URL = "http://localhost:5000"//import.meta.env.VITE_API_URL as string;

export const protectedFetch = async <T>(url: string, options: RequestInit) => {
	console.log("fetching" + url + options);
	const res = await fetch(url, options);
	console.log("response", res);
	const json = await res.json();
	console.log("json" + json)
	if (!res.ok) throw json;
	return json as T;
};
