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
