import { RefObject } from "react";

export interface IUser {
  id: string;
  username: string;
  accessToken: string;
  refreshToken: string;
}

export interface ILoginResponseBody {
  ID?: string;
  Username?: string;
  AccessToken?: string;
  RefreshToken?: string;
}

export interface ILogFn {
  (message: any, ...optionalParams: any[]): void;
}

export interface ILogger {
  debug: ILogFn;
  info: ILogFn;
  warn: ILogFn;
  error: ILogFn;
}

export interface IExplanation {
  Expression: string;
  Position: number;
  Description?: string;
}

export interface IPhrase {
  refs: RefObject<HTMLSpanElement>[];
  explanation: "";
}

export interface IDashboardState {
  inputText: string;
  showInput: boolean;
  blocks: React.ReactNode[] | null;
  blockRefs: (RefObject<HTMLSpanElement> | null)[] | null;
  selectedIndices: number[];
  phrases: IPhrase[];
}
