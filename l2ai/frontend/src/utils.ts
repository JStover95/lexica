const crossorigin = Boolean(process.env.CROSSORIGIN);


export const scrollToMiddle = (container: HTMLElement, element: HTMLElement) => {
  // Get the container's dimensions and scroll position
  const containerRect = container.getBoundingClientRect();
  const elementRect = element.getBoundingClientRect();
  
  // Calculate the offset to center the element within the container
  const offsetTop = elementRect.top - containerRect.top - containerRect.height / 2 + elementRect.height / 2;
  
  // Scroll the container to the calculated offset
  container.scrollBy({
      top: offsetTop,
      behavior: 'smooth' // Optional: Adds smooth scrolling animation
  });
}


export const scrollToTop = (container: HTMLElement, element: HTMLElement) => {
  // Get the container's dimensions and scroll position
  const containerRect = container.getBoundingClientRect();
  const elementRect = element.getBoundingClientRect();
  
  // Calculate the offset to center the element within the container
  const offsetTop = elementRect.top - containerRect.top;
  
  // Scroll the container to the calculated offset
  container.scrollBy({
      top: offsetTop,
      behavior: 'smooth' // Optional: Adds smooth scrolling animation
  });
}


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
