import { IResponseBody } from "./interfaces";

const crossorigin = Boolean(process.env.CROSSORIGIN);


// make a request with options
// TODO: implement CSRF protection
export const makeRequest = async (url: string, opts?: any): Promise<any> => {
  const csrfToken = localStorage.getItem("csrfToken");

  // set credentials and crossorigin options
  if (opts) opts.crossorigin = crossorigin;
  else opts = {crossorigin: crossorigin}

  const jwt = localStorage.getItem("AccessToken");
  if (jwt) {
    if (opts.headers) opts.headers["Authorization"] = `Bearer ${jwt}`;
    else opts.headers = {"Authorization": `Bearer ${jwt}`};
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
      const body: IResponseBody = await res.json();

      if (res.status == 200 && body.CSRFToken)
        localStorage.setItem("csrfToken", body.CSRFToken);
      if (res.status == 200 && body.AccessToken)
        localStorage.setItem("AccessToken", body.AccessToken);
      if (res.status == 200 && body.RefreshToken)
        localStorage.setItem("RefreshToken", body.RefreshToken);

      // TODO: handle server errors
      return body;
    }
  );
};
