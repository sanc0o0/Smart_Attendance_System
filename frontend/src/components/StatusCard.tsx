import Skeleton from "./Skeleton";

type Props = {
    status: {
        date: string;
        session: string | null;
        session_open: boolean;
        is_holiday: boolean;
        is_weekend: boolean;
        holiday_reason: string | null;
        opens_at: string | null;
        closes_at: string | null;
    };
};

function getStatusUI(status: Props["status"]) {
    if (status.is_holiday) {
        return {
            label: "HOLIDAY",
            color: "border-yellow-500 bg-yellow-50 text-yellow-900",
            badge: "bg-yellow-500",
            hint: status.holiday_reason ?? "No sessions today",
        };
    }

    if (status.session_open) {
        return {
            label: "OPEN",
            color: "border-green-600 bg-green-50 text-green-900",
            badge: "bg-green-600",
            hint: `${status.session?.toUpperCase()} session active`,
        };
    }


    return {
        label: "CLOSED",
        color: "border-red-600 bg-red-50 text-red-900",
        badge: "bg-red-600",
        hint: "No active session",
    };
}

export default function StatusCard({ status }: Props) {
    const ui = getStatusUI(status);

    if (!status) {
        return (
            <div className="bg-yellow-50 border rounded-xl p-6">
                <Skeleton height="h-5" width="w-1/3" />
                <div className="mt-3 space-y-2">
                    <Skeleton height="h-4" />
                    <Skeleton height="h-4" />
                </div>
            </div>
        );
    }    

    return (
        <div className={`border-2 rounded-xl p-6 ${ui.color}`}>
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">Session Status</h2>

                <span
                    className={`px-3 py-1 text-sm font-bold text-white rounded-full ${ui.badge}`}
                >
                    {ui.label}
                </span>
            </div>

            <div className="space-y-1 text-sm">
                <p><strong>Date:</strong> {status.date}</p>
                <p><strong>Session:</strong> {status.session ?? "None"}</p>

                {status.opens_at && status.closes_at && (
                    <p className="text-xs opacity-80">
                        Time Window: {status.opens_at} – {status.closes_at}
                    </p>
                )}
            </div>

            <p className="mt-4 text-sm italic opacity-90">
                {ui.hint}
            </p>
        </div>
    );
}
  