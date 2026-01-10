import {
    getSessionStatus,
    getTodayAnalytics,
    getStudentAnalytics,
} from "@/src/lib/api";

import StatusCard from "@/src/components/StatusCard";
import AnalyticsCard from "@/src/components/AnalyticsCard";
import StudentTable from "@/src/components/StudentTable";
import AdminSessionControls from "@/src/components/AdminSessionControls";
import Skeleton from "@/src/components/Skeleton";

export default async function AdminPage() {
    const [status, today, students] = await Promise.all([
        getSessionStatus(),
        getTodayAnalytics(),
        getStudentAnalytics(),
    ]);

    return (
        <main className="max-w-5xl mx-auto p-6 space-y-8 text-black">
            <header>
                <h1 className="text-3xl font-bold text-white">Admin Dashboard</h1>
                <p className="text-gray-500">
                    Date: {new Date(status.date).toDateString()}
                </p>
            </header>

            <StatusCard status={status} />

            <AdminSessionControls status={status} />

            {!today?(
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-6">
                    {[1, 2, 3].map((i) => (
                        <div
                            key={i}
                            className="bg-white rounded-xl shadow-sm px-6 py-5"
                        >
                            <Skeleton height="h-4" width="w-1/2" />
                            <div className="mt-4">
                                <Skeleton height="h-8" width="w-1/3" />
                            </div>
                        </div>
                    ))}
                </div>
            ):(
                <section className="grid grid-cols-1 md:grid-cols-3 gap-4 text-black">
                    <AnalyticsCard title="Morning Attendance" value={today.morning} accent="blue"/>
                    <AnalyticsCard title="Afternoon Attendance" value={today.afternoon} accent="blue" />
                    <AnalyticsCard title="Total Attendance" value={today.total} accent="green"/>
                </section>
            )}

            {!students ? (
                <div className="bg-white rounded-xl shadow-sm mt-8 p-6 space-y-4">
                    {[1, 2, 3, 4].map((i) => (
                        <Skeleton key={i} height="h-6" />
                    ))}
                </div>
            ) : (
                <StudentTable data={students} />
            )}

        </main>
    );
 }
  