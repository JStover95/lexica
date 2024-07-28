import { APP_ENV } from "./environment";

export interface LogFn {
  (message: any, ...optionalParams: any[]): void;
}

export interface ILogger {
  debug: LogFn;
  info: LogFn;
  warn: LogFn;
  error: LogFn;
}

export type LogLevel = "debug" | "info" | "warn" | "error";

function isValidLogLevel(level: any): level is LogLevel {
  return ["debug", "info", "warn", "error"].includes(level);
}

function getLogLevel(): LogLevel {
  const level = process.env.LOG_LEVEL;
  if (level && isValidLogLevel(level)) {
    return level;
  } else if (level) {
    throw new Error(`Invalid LOG_LEVEL: ${level}. Must be one of "debug", "info", "warn", "error".`);
  }
  return "info";
}

export const LOG_LEVEL: LogLevel = (
  APP_ENV === "production" ? "warn" : getLogLevel()
);


const NO_OP: LogFn = (message?: any, ...optionalParams: any[]) => {};


/** Logger which outputs to the browser console */
export class Logger implements ILogger {
  readonly debug: LogFn;
  readonly info: LogFn;
  readonly warn: LogFn;
  readonly error: LogFn;

  constructor(options?: { levelName: LogLevel }) {
    const levelMap: Record<LogLevel, number> = {
      debug: 1, info: 2, warn: 3, error: 4
    };
    const levelName: LogLevel = options?.levelName || "warn";
    const level: number = levelMap[levelName];

    this.error = console.error.bind(console);
    this.warn = level <= 3 ? console.warn.bind(console) : NO_OP;
    this.info = level <= 2 ? console.log.bind(console) : NO_OP;
    this.debug = level <= 1 ? console.debug.bind(console) : NO_OP;
  }
}


export const logger = new Logger({ levelName: LOG_LEVEL });
