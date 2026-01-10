"use client";

import { openSession, closeSession } from "@/src/lib/api";
import { useRouter } from "next/navigation";
import { SessionStatus } from "../types/session";
import { useState } from "react";
import toast, { Toaster } from "react-hot-toast";


type Props = {
    status: SessionStatus;
};

export default function AdminSessionControls({ status }: Props) {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const {session, session_open, is_holiday} = status;
    
    const canOpenMorning =
    !is_holiday &&
    !session_open &&
    session !== "morning" || session === null;
    
    const canOpenAfternoon = 
    !is_holiday &&
    !session_open &&
    session !== "afternoon" || session === null;
    
    const canClose =
    !is_holiday &&
    session !== null &&
    session_open;
    
    async function handleOpen(session: "morning" | "afternoon") {
        try {
            setLoading(true);
            await openSession(session);
            toast.success(`${session} session opened successfully`);
            router.refresh();
        } catch (error: unknown) {
            const message = error instanceof Error ? error.message : String(error);
            toast.error(
                message ||
                `Cannot open ${session} session outside time window`
            );
        } finally{
            setLoading(false);
        }
    }

    async function handleClose() {
        if (!session) return;

        try {
            setLoading(true);
            await closeSession(session);
            toast.success("Session closed");
            router.refresh();
        } catch(error: unknown) {
            const message = error instanceof Error ? error.message : String(error);
            toast.error(message || "Cannot close session before time");
        } finally {
            setLoading(false);
        } 
    }

    return (
        <div className="flex flex-wrap gap-4 mt-4 items-center">
            <button
                onClick={() => handleOpen("morning")}
                disabled={!canOpenMorning || loading}
                className={`px-4 py-2 rounded font-medium
            ${canOpenMorning
                        ? "bg-green-600 hover:bg-green-700 text-white"
                        : "bg-gray-300 text-gray-600 cursor-not-allowed"}
        `}
            >
                Open Morning
            </button>

            <button
                onClick={() => handleOpen("afternoon")}
                disabled={!canOpenAfternoon || loading}
                className={`px-4 py-2 rounded font-medium
            ${canOpenAfternoon
                        ? "bg-green-600 hover:bg-green-700 text-white"
                        : "bg-gray-300 text-gray-600 cursor-not-allowed"}
        `}
            >
                Open Afternoon
            </button>

            <button
                onClick={handleClose}
                disabled={!canClose || loading}
                className={`px-4 py-2 rounded font-medium
            ${canClose
                        ? "bg-red-600 hover:bg-red-700 text-white"
                        : "bg-gray-300 text-gray-600 cursor-not-allowed"}
        `}
            >
                Close Session
            </button>

            <p className="mt-3 text-xs text-gray-400">
                Sessions can only be opened during valid time windows.
                Admin overrides are still subject to system rules.
            </p>

            {loading && (
                <span className="text-sm text-gray-400 ml-2">
                    Applying changes…
                </span>
            )}
        </div>

    );
}
