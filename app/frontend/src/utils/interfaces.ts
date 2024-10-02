import { RefObject } from "react";

export interface IBaseResponseBody {
  Message: string;
}

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
  text: string;
  context: string;
  previousText: string;
  active: boolean;
  startIndex: number;
  stopIndex: number;
  dictionaryEntries: { query: string; entries: IDictionaryEntry[] }[];
}

export interface IDashboardState {
  inputText: string;
  showInput: boolean;
  blocks: React.ReactNode[] | null;
  blockRefs: (RefObject<HTMLSpanElement> | null)[] | null;
  selectedIndices: number[];
  phrases: IPhrase[];
}

export interface IReadState {
  blocks: React.ReactNode[] | null;
  blockRefs: (RefObject<HTMLSpanElement> | null)[] | null;
  selectedIndices: number[];
  phrases: IPhrase[];
}

export interface IEquivalent {
  equivalentLanguage: string;
  equivalent: string;
  definition: string;
}

export interface ISense {
  senseNo?: string;
  definition: string;
  partOfSpeech?: string;
  examples?: string[];
  type?: string;
  equivalents?: IEquivalent[];
  rank?: number;
}

export interface ISeenContent {
  _id: string;
  text: string;
  indices: number[][];
}

export interface IDictionaryEntry {
  sourceId?: string;
  sourceLanguage?: string;
  writtenForm: string;
  variations?: string[];
  partOfSpeech: string;
  grade?: string;
  queryStrs?: string[];
  senses: ISense[];
  showAll?: boolean;
  seenContent?: ISeenContent[];
}

export interface IInferResponseBody extends IBaseResponseBody {
  Result: IDictionaryEntry[];
}

export interface ISeenContentResponseBody extends IBaseResponseBody {
  Result: ISeenContent[];
}
