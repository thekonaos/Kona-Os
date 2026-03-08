export type OsVerdict = "KERNEL" | "ROOT" | "SYSTEM" | "USER" | "IDLE" | "CRASHED";
export interface OsMetrics { signal_clarity:number; process_health:number; kernel_stability:number; routing_efficiency:number; memory_score:number; }
export interface KernelReport { contract_address:string; metrics:OsMetrics; verdict:OsVerdict; process_id:string; log:string[]; uptime_score:number; final_score:number; }
