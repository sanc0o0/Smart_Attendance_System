export type SessionStatus = {
    date: string | Date;
    session: "morning" | "afternoon" | null;
    session_open: boolean;
    opened_at?: string | Date;
    manual?: boolean;
};

export type TodayAnalytics = {
    date: string | Date;
    morning: number;
    afternoon: number;
    total: number;
};

export type StudentAnalytics = {
    name: string;
    total_days: number;
};
