import useAuth from "./hooks/useAuth";

const crossorigin = Boolean(process.env.CROSSORIGIN);


// make a request with options
// TODO: implement CSRF protection
export const makeRequest = async (url: string, opts?: any): Promise<any> => {
  const csrfToken = localStorage.getItem("csrfToken");
  const { accessToken } = useAuth();

  if (opts) opts.crossorigin = crossorigin;
  else opts = { crossorigin: crossorigin }

  if (accessToken) {
    if (opts.headers) opts.headers["Authorization"] = `Bearer ${accessToken}`;
    else opts.headers = { "Authorization": `Bearer ${accessToken}` };
  }

  // if making a POST request
  if (opts && opts.method == "POST") {

    // set the content type and CSRF token headers
    if (opts.headers) {
      opts.headers["Content-Type"] = "application/json";
      opts.headers["X-CSRF-Token"] = csrfToken;
    } else
      opts.headers = {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrfToken
      };
  }

  // make the request
  return fetch(process.env.API_ENDPOINT + url, opts ? opts : {}).then(
    async (res) => {
      const body = await res.json();

      if (res.status == 200 && body.CSRFToken)
        localStorage.setItem("csrfToken", body.CSRFToken);

      // TODO: handle server errors
      return body;
    }
  );
};
