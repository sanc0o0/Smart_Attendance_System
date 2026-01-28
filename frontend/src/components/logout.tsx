"use client";

import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

export default function LogoutButton() {
    const router = useRouter();

    function logout() {
        localStorage.removeItem("adminAuth");
        router.push("/login");
        toast.success("Logged out successfully")
    }

    return (
        <button
            onClick={logout}
            className="bg-red-600 h-fit hover:bg-red-700 text-white px-4 py-2 rounded font-medium"
        >
            Logout
        </button>
    );
}
