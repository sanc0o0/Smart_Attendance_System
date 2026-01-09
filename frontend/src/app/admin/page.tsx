import {
    getSessionStatus,
    getTodayAnalytics,
    getStudentAnalytics,
} from "@/src/lib/api";

import StatusCard from "@/src/components/StatusCard";
import AnalyticsCard from "@/src/components/AnalyticsCard";
import StudentTable from "@/src/components/StudentTable";
import AdminSessionControls from "@/src/components/AdminSessionControls";

export default async function AdminPage() {
    const [status, today, students] = await Promise.all([
        getSessionStatus(),
        getTodayAnalytics(),
        getStudentAnalytics(),
    ]);

    return (
        <main className="p-8 max-w-5xl mx-auto space-y-6 text-black">
            <h1 className="text-3xl font-bold text-white">Admin Dashboard</h1>

            <StatusCard status={status} />

            <div className="grid grid-cols-3 gap-4">
                <AnalyticsCard title="Morning" value={today.morning} />
                <AnalyticsCard title="Afternoon" value={today.afternoon} />
                <AnalyticsCard title="Total" value={today.total} />
            </div>

            <StudentTable data={students} />

            <AdminSessionControls status={status} />
        </main>
    );
}
  