export type Environment = 'development' | 'production';
export const APP_ENV: Environment = (
  process.env.REACT_APP_APP_ENV === 'production' ? 'production' : 'development'
);
