const crossorigin = Boolean(process.env.CROSSORIGIN);

export const highlightSubstrings = (s: string, indices: number[][]) => {
  return indices.map(([start, stop], index) => {
    const highlightText = s.slice(start, stop + 1);

    // Find the start of the sentence containing the highlight by going backwards to the previous period
    let sentenceStart = s.lastIndexOf('.', start) + 1;
    // Move the index past any spaces after the period
    while (s[sentenceStart] === ' ' || s[sentenceStart] === "\"") sentenceStart++;

    let sentenceEnd = s.indexOf('.', stop) + 1;
    while (s[sentenceEnd] === "\"") sentenceEnd++;

    // Get the surrounding text with highlight centered when possible
    const left = s.slice(sentenceStart, start);
    const right = s.slice(stop + 1, sentenceEnd);

    return (
      <span key={`seen-content-highlight-${index}`} className="mb-2">
          {left}<b>{highlightText}</b>{right}
      </span>
    );
  });
};

/**
 * Scrolls the given container so that the specified element is aligned either 
 * with the top edge of the container (if the element is larger than the container),
 * or ensures the entire element is visible (if the element is smaller).
 * 
 * @param {HTMLElement} container - The container element that should be scrolled.
 * @param {HTMLElement} element - The target element to be aligned with the top of the container.
 */
export const scrollToTop = (container: HTMLElement, element: HTMLElement) => {
  const containerRect = container.getBoundingClientRect();
  const elementRect = element.getBoundingClientRect();
  
  const relativeOffset = elementRect.top - containerRect.top;
  
  // Check if the element is smaller than the container
  const elementHeight = elementRect.height;
  const containerHeight = containerRect.height;

  // If the element is smaller, scroll just enough to bring the bottom of the element into view
  if (elementHeight < containerHeight) {
    const scrollAmount = relativeOffset - (containerHeight - elementHeight);
    container.scrollBy({
      top: scrollAmount + 16,
      behavior: "smooth",
    });
  } else {
    // Default behavior, scroll to the top of the element
    container.scrollBy({
      top: relativeOffset - 8,
      behavior: "smooth",
    });
  }
};


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
