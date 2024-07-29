const crossorigin = Boolean(process.env.CROSSORIGIN);


// make a request with options
// TODO: implement CSRF protection
export const makeRequest = async (opts: {
  url: string,
  accessToken?: string,
  options?: any
}): Promise<[number, any]> => {
  const csrfToken = localStorage.getItem("csrfToken");
  const { url, accessToken } = opts
  let { options } = opts;

  if (options) options.crossorigin = crossorigin;
  else options = { crossorigin: crossorigin }

  if (accessToken) {
    if (options.headers)
      options.headers["Authorization"] = `Bearer ${accessToken}`;
    else options.headers = { "Authorization": `Bearer ${accessToken}` };
  }

  // if making a POST request
  if (options && options.method === "POST") {

    // set the content type and CSRF token headers
    if (options.headers) {
      options.headers["Content-Type"] = "application/json";
      options.headers["X-CSRF-Token"] = csrfToken;
    } else
      options.headers = {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrfToken
      };
  }

  // make the request
  return fetch(process.env.API_ENDPOINT + url, options ? options : {}).then(
    async (res) => {
      const body = await res.json();

      if (res.status === 200 && body.CSRFToken)
        localStorage.setItem("csrfToken", body.CSRFToken);

      // TODO: handle server errors
      return [res.status, body];
    }
  );
};
