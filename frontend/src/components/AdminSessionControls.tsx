"use client";

import { openSession, closeSession } from "@/src/lib/api";
import { useRouter } from "next/navigation";
import { SessionStatus } from "../types/session";


type Props = {
    status: SessionStatus;
};

export default function AdminSessionControls({ status }: Props) {
    const router = useRouter();
    const {session, session_open, is_holiday} = status;
    
    const canOpenMorning =
    !is_holiday &&
    session !== "morning";
    
    const canOpenAfternoon = 
    !is_holiday &&
    session !== "afternoon";
    
    const canClose =
    !is_holiday &&
    session !== null &&
    session_open;
    
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
        if (!session) return;
        await closeSession(session);
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
