export type SessionName = "morning" | "afternoon";

export type SessionStatus = {
    date: string ;
    current_time: string ;

    // holiday info
    is_holiday: boolean;
    holiday_reason: string | null;

    // session info
    session: SessionName | null;
    session_open: boolean;

    // time windows info
    opens_at: string | null;
    closes_at: string | null;

    // admin override
    manual_override: boolean;
};

export type TodayAnalytics = {
    date: string ;
    morning: number;
    afternoon: number;
    total: number;
};

export type StudentAnalytics = {
    name: string;
    total_days: number;
};
