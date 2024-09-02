import { Environment } from "./types";

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      REACT_APP_API_ENDPOINT: string;
    }
  }
}

export const APP_ENV: Environment = (
  process.env.REACT_APP_APP_ENV === "production" ? "production" : "development"
);
