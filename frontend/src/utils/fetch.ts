export const API_URL = "http://127.0.0.1:8000";

export const protectedFetch = async <T>(url: string, options: RequestInit) => {
	console.log("fetching" + url + options);
	const res = await fetch(url, options);
	console.log("response", res);
	const json = await res.json();
	console.log("json" + json)
	if (!res.ok) throw json;
	return json as T;
};
