import { COGNITO_REDIRECT_URI } from "../environment.d";

const authConfig = {
  domain: process.env.REACT_APP_COGNITO_DOMAIN,
  clientId: process.env.REACT_APP_COGNITO_APP_CLIENT_ID,
  redirectUri: COGNITO_REDIRECT_URI,
  logoutUri: COGNITO_REDIRECT_URI,  // TODO: Set this to a unique URI for logging out
  scope: "email",
  responseType: "code",
};

/**
 * The React hook for handling authentication with AWS Cognito.
 */
const useAuth = () => {

  /**
   * This function checks whether the current user is authenticated. A valid
   * access token or refresh token are assumed to be stored in the user's
   * cookies for validation by the server.
   * 
   * This function attempts to obtain a new access token using the user's
   * refresh token if the access token cannot be validated.
   * 
   * This function will return false if the user's access token cannot be
   * validated and a new access token cannot be created with a refresh token and
   * returns true if the user can be authenticated.
   * 
   * @returns (boolean) Whether the current user is authenticated.
   */
  const checkAuth = async () => {
    try {
      const url = `${process.env.REACT_APP_API_ENDPOINT}/verify-token`;
      const response = await fetch(url, {
        method: "POST",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Token invalid or expired");
      }

      return true;
    } catch (error) {
      // TODO: only try to refresh when a refresh token is present
      // Try refreshing the token
      try {
        const url = `${process.env.REACT_APP_API_ENDPOINT}/refresh-token`;
        const response = await fetch(url, {
          method: "POST",
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Token expired");
        }

        return true;
      } catch (error) {
        console.error("Authentication check failed:", error);
      }
    }

    return false;
  };

  /**
   * This function attempts to exchange the `id_code` received from the AWS
   * Cognito hosted UI for an access token. Returns true if this is successful
   * and false otherwise.
   * 
   * This function should be called from a valid callback endpoint that can
   * retrieve the `code` search parameter from the URl on redirect from Cognito.
   * 
   * @param code (string) The `id_code` returned from the AWS Cognito hsoted UI.
   * @returns (boolean) Whether the `id_code` was successfully exchanged for an
   *  access token.
   */
  const handleAuthCallback = async (code: string) => {
    try {
      const url = `${process.env.REACT_APP_API_ENDPOINT}/token-exchange`;
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
        credentials: "include",
      });

      if (!response.ok) {
        throw Error("Failed to authenticate.");
      }

      return true;
    } catch (error) {
      console.error("Error:", error);
    }

    return false;
  };

  // Redirect the user to the AWS Cognito hosted UI for logging in.
  const login = () => {
    const url = new URL(`https://${authConfig.domain}/login`);
    const params = new URLSearchParams(url.search);
    params.append("client_id", authConfig.clientId);
    params.append("scope", authConfig.scope);
    params.append("response_type", authConfig.responseType);
    params.append("redirect_uri", authConfig.redirectUri);
    url.search = params.toString();
    window.location.href = url.toString();
  };

  // Redirect the user to the AWS Cognito logout endpoint.
  const logout = () => {
    const url = new URL(`https://${authConfig.domain}/logout`);
    const params = new URLSearchParams(url.search);
    params.append("client_id", authConfig.clientId);
    params.append("logout_uri", authConfig.logoutUri);
    url.search = params.toString();
    window.location.href = url.toString();
  };

  return { handleAuthCallback, checkAuth, login, logout };
};


export default useAuth;
