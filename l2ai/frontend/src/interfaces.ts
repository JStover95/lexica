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
