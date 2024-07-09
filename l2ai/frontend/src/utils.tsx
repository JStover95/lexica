import { IResponseBody, IUser } from "./interfaces";

const crossorigin = Boolean(process.env.CROSSORIGIN);


// make a request with options
// TODO: implement CSRF protection
export const makeRequest = async (url: string, opts?: any): Promise<any> => {
  const csrfToken = localStorage.getItem("csrfToken");

  // set credentials and crossorigin options
  if (opts) opts.crossorigin = crossorigin;
  else opts = {crossorigin: crossorigin}

  const accessToken = localStorage.getItem("accessToken");
  if (accessToken) {
    if (opts.headers) opts.headers["Authorization"] = `Bearer ${accessToken}`;
    else opts.headers = {"Authorization": `Bearer ${accessToken}`};
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
        localStorage.setItem("accessToken", body.AccessToken);
      if (res.status == 200 && body.RefreshToken)
        localStorage.setItem("refreshToken", body.RefreshToken);

      // TODO: handle server errors
      return body;
    }
  );
};


export const getCurrentAuthenticatedUser = async (): Promise<IUser> => {
  let res = await makeRequest("/verify");

  if (res.IsAuthenticated) {
    const user: IUser = {"Username": res.Username};
    return user
  }

  const accessToken = localStorage.getItem("accessToken");
  const refreshToken = localStorage.getItem("refreshToken");
  const body = {"AccessToken": accessToken, "RefreshToken": refreshToken}
  const opts = {"method": "POST", "body": JSON.stringify(body)}
  res = await makeRequest("/refresh", opts);

  if (res.IsAuthenticated) {
    const user: IUser = {"Username": res.Username};
    return user
  }

  throw "Unauthorized request";
}
