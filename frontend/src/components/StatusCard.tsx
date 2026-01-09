type Props = {
    status: {
        date: string;
        session: string | null;
        session_open: boolean;
    };
};

export default function StatusCard({ status }: Props) {
    return (
        <div className="p-4 bg-white rounded-2xl shadow">
            <h2 className="font-semibold text-lg mb-2">Session Status</h2>
            <p>Date: {status.date}</p>
            <p>Session: {status.session ?? "None"}</p>
            <p>Status: {status.session_open ? "OPEN" : "CLOSED"}</p>
        </div>
    );
}
  