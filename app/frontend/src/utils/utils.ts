const crossorigin = Boolean(process.env.CROSSORIGIN);


/**
 * Scrolls the given container so that the specified element is aligned with the
 * top edge of the container.
 * 
 * @param {HTMLElement} container - The container element that should be
 *  scrolled.
 * @param {HTMLElement} element - The target element to be aligned with the top
 *  of the container.
 */
export const scrollToTop = (container: HTMLElement, element: HTMLElement) => {
  const elementRect = element.getBoundingClientRect();
  container.scrollTo({
      top: elementRect.top,
      behavior: "smooth"
  });
}

/**
 * Makes a network request with the specified options and returns the response
 * status and body.
 * 
 * @param {Object} opts - The options for the request.
 * @param {string} opts.url - The URL to request.
 * @param {string} [opts.accessToken] - The access token for authorization
 *  (optional).
 * @param {Object} [opts.options] - Additional options for the request
 *  (optional).
 * @returns {Promise<[number, any]>} A promise that resolves to a tuple
 *  containing the response status and response body.
 * 
 * @throws {Error} Will throw an error if the request fails.
 */
export const makeRequest = async (opts: {
  url: string,
  accessToken?: string,
  options?: any
}): Promise<[number, any]> => {
  const csrfToken = localStorage.getItem("csrfToken");
  const { url, accessToken } = opts
  let { options } = opts;

  // Set cross origin option
  if (options) options.crossorigin = crossorigin;
  else options = { crossorigin: crossorigin }

  // If an access token was passed as an argument, include it in a Bearer Authorization header
  if (accessToken) {
    if (options.headers)
      options.headers["Authorization"] = `Bearer ${accessToken}`;
    else options.headers = { "Authorization": `Bearer ${accessToken}` };
  }

  // If making a POST request
  if (options && options.method === "POST") {

    // Set the content type and CSRF token headers
    if (options.headers) {
      options.headers["Content-Type"] = "application/json";
    } else {
      options.headers = {
        "Content-Type": "application/json",
      };
    }
    if (csrfToken) options.headers["X-CSRF-Token"] = csrfToken;
  }

  // Make the request
  return fetch(process.env.REACT_APP_API_ENDPOINT + url, options ? options : {}).then(
    async (res) => {
      const body = await res.json();

      // Save a CSRF Token if one was received from the server
      if (res.status === 200 && body.CSRFToken)
        localStorage.setItem("csrfToken", body.CSRFToken);

      // TODO: Handle server errors
      return [res.status, body];
    }
  );
};
