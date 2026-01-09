"use client";

import { openSession, closeSession } from "@/src/lib/api";
import { useRouter } from "next/navigation";


type Props = {
    status: {
        session: "morning" | "afternoon" | null;
        session_open: boolean;
        is_holiday: boolean;
    };
};

export default function AdminSessionControls({ status }: Props) {
    const router = useRouter();

    const canOpenMorning =
        !status.session_open &&
        !status.is_holiday &&
        status.session === null;

    const canOpenAfternoon = 
        !status.session_open &&
        !status.is_holiday &&
        status.session === null;

    const canClose =
        status.session_open;

    async function handleOpen(session: "morning" | "afternoon") {
        try {
            await openSession(session);
            router.refresh();
        } catch (error: unknown) {
            const message = error instanceof Error ? error.message : String(error);
            alert(`Attendance not allowed outside the time window: ${message}`);   
        }
    }
    async function handleClose() {
        if (!status.session) return;
        await closeSession(status.session);
        router.refresh();
    }

    return (
        <div className="flex gap-4 mt-4">
            <button
                onClick={() => handleOpen("morning")}
                disabled={!canOpenMorning}
                className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50 cursor-pointer"
            >
                Open Morning
            </button>

            <button
                onClick={() => handleOpen("afternoon")}
                disabled={!canOpenAfternoon}
                className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50 cursor-pointer"
            >
                Open Afternoon
            </button>

            <button
                onClick={handleClose}
                disabled={!canClose}
                className="px-4 py-2 bg-red-600 text-white rounded disabled:opacity-50 cursor-pointer"
            >
                Close Session
            </button>
        </div>
    );
}
