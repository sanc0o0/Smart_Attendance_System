import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="max-w-xl text-center space-y-6 px-4">
        <h1 className="text-4xl font-bold">
          Smart Attendance System
        </h1>

        <p className="text-gray-400">
          An automated attendance management platform with
          role-based admin controls and real-time session monitoring.
        </p>

        <div className="flex justify-center gap-4">
          <Link
            href="/login"
            className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded font-medium"
          >
            Admin Login
          </Link>

          <Link
            href="/admin"
            className="border border-gray-600 hover:bg-gray-800 px-6 py-2 rounded font-medium"
          >
            Dashboard
          </Link>
        </div>

        <p className="text-xs text-gray-500 pt-6">
          Built with Next.js, FastAPI, PostgreSQL
        </p>
      </div>
    </main>
  );
}
