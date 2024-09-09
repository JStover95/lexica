import { Environment } from "./utils/types";

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      REACT_APP_APP_ENV: string;
      REACT_APP_API_ENDPOINT: string;
      REACT_APP_COGNITO_DOMAIN: string;
      REACT_APP_COGNITO_APP_CLIENT_ID: string;
      REACT_APP_COGNITO_REDIRECT_URI: string;
    }
  }
}

export const APP_ENV: Environment = (
  process.env.REACT_APP_APP_ENV === "production" ? "production" : "development"
);

export const COGNITO_REDIRECT_URI = (
  process.env.REACT_APP_APP_ENV === "production"
    ? process.env.REACT_APP_COGNITO_REDIRECT_URI
    : "http://localhost:3000/"
);
