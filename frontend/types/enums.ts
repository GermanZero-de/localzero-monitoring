export enum ExecutionStatus {
    UNKNOWN = 0,
    AS_PLANNED = 2,
    COMPLETE = 4,
    DELAYED = 6,
    FAILED = 8,
  }

  export enum TaskStatus {
    complete = "complete",
    asPlanned = "asPlanned",
    delayed = "delayed",
    failed = "failed",
    unknown = "unknown",
  }

  export enum TaskSource {
    kap = 0,
    suggested = 1
  }

