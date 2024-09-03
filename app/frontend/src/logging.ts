import { APP_ENV } from "./environment";
import { ILogFn, ILogger } from "./interfaces";
import { LogLevel } from "./types";


/**
 * Checks if a given log level is valid.
 * 
 * @param level - The level to validate.
 * @returns `true` if the level is valid, otherwise `false`.
 */
function isValidLogLevel(level: any): level is LogLevel {
  return ["debug", "info", "warn", "error"].includes(level);
}


/**
 * Retrieves the log level from the environment.
 * 
 * @returns The log level specified in the environment or "info" if not set or
 *  invalid.
 * @throws Will throw an error if the LOG_LEVEL is set and is invalid.
 */
function getLogLevel(): LogLevel {
  const level = process.env.LOG_LEVEL;
  if (level && isValidLogLevel(level)) {
    return level;
  } else if (level) {
    throw new Error(`Invalid LOG_LEVEL: ${level}. Must be one of "debug", "info", "warn", "error".`);
  }
  return "info";
}

// Determine the log level based on the application environment.
export const LOG_LEVEL: LogLevel = (
  APP_ENV === "production" ? "warn" : getLogLevel()
);

// No-operation logger function for levels that should not log anything.
const NO_OP: ILogFn = (message?: any, ...optionalParams: any[]) => {};


/**
 * Logger class implementing the ILogger interface.
 * Provides methods for various log levels: debug, info, warn, and error.
 */
export class Logger implements ILogger {
  readonly debug: ILogFn;
  readonly info: ILogFn;
  readonly warn: ILogFn;
  readonly error: ILogFn;

  /**
   * Initializes the Logger instance with a specified log level.
   * 
   * @param options - Optional configuration object specifying the log level.
   */
  constructor(options?: { levelName: LogLevel }) {
    // Mapping log levels to numerical values for comparison.
    const levelMap: Record<LogLevel, number> = {
      debug: 1, info: 2, warn: 3, error: 4
    };
    // Determine the log level to use. Default is "warn".
    const levelName: LogLevel = options?.levelName || "warn";
    const level: number = levelMap[levelName];

    // Assign logging functions based on the specified log level.
    this.error = console.error.bind(console);
    this.warn = level <= 3 ? console.warn.bind(console) : NO_OP;
    this.info = level <= 2 ? console.log.bind(console) : NO_OP;
    this.debug = level <= 1 ? console.debug.bind(console) : NO_OP;
  }
}

// Export a logger instance with the configured log level.
export const logger = new Logger({ levelName: LOG_LEVEL });
