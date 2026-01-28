"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

const ADMIN_EMAIL = "admin@test.com";
const ADMIN_PASSWORD = "admin123"; // change later

export default function LoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    function handleLogin(e: React.FormEvent) {
        e.preventDefault();

        if (email !== ADMIN_EMAIL || password !== ADMIN_PASSWORD) {
            toast.error("Invalid Credentials")
            setError("Invalid email or password");
            return;
        }

        toast.success("Welcome Admin!")

        const expiresAt = Date.now() + 60 * 60 * 1000; // 1 hour

        localStorage.setItem(
            "adminAuth",
            JSON.stringify({ email, expiresAt })
        );

        router.push("/admin");
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-black text-white">
            <form
                onSubmit={handleLogin}
                className="w-full max-w-sm bg-neutral-900 p-6 rounded-xl space-y-4"
            >
                <h1 className="text-2xl font-bold text-center">Admin Login</h1>

                {error && (
                    <p className="text-red-400 text-sm text-center">{error}</p>
                )}

                <input
                    type="email"
                    placeholder="Admin email"
                    className="w-full px-4 py-2 rounded bg-neutral-800"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <input
                    type="password"
                    placeholder="Password"
                    className="w-full px-4 py-2 rounded bg-neutral-800"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button
                    type="submit"
                    className="w-full py-2 rounded bg-blue-600 hover:bg-blue-700"
                >
                    Login
                </button>

                <p
                    className="text-sm text-center text-gray-400 cursor-pointer"
                >
                    Not an Admin?
                </p>
                <p
                    className="text-sm text-center text-gray-400 cursor-pointer hover:underline"
                    onClick={() => router.push("/register")}
                >
                    Get in touch with organizer
                </p>
            </form>
        </div>
    );
}
