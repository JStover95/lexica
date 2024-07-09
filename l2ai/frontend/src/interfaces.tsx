export interface IResponseBody {
  Message: string;
  CSRFToken?: string;
  AccessToken?: string;
  RefreshToken?: string;
}

export interface IUser {
  Username: string;
}
