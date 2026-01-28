"use client";

import { useState } from "react";

function getInitialAdminState(): boolean {
    if (typeof window === "undefined") return false;

    const raw = localStorage.getItem("adminAuth");
    if (!raw) return false;

    try {
        const parsed = JSON.parse(raw);
        return Date.now() < parsed.expiresAt;
    } catch {
        return false;
    }
}

export default function Navbar() {
    const [isAdmin] = useState(getInitialAdminState);

    return (
        <nav>
            {isAdmin ? (
                <a href="/admin">Admin</a>
            ) : (
                <a href="/login">Login</a>
            )}
        </nav>
    );
}

// "use client";

// import { useEffect, useState } from "react";

// export default function Navbar() {
//     const [isAdmin, setIsAdmin] = useState<boolean | null>(null);

//     useEffect(() => {
//         const raw = localStorage.getItem("adminAuth");
//         if (!raw) {
//             setIsAdmin(false);
//             return;
//         }

//         try {
//             const parsed = JSON.parse(raw);
//             setIsAdmin(Date.now() < parsed.expiresAt);
//         } catch {
//             setIsAdmin(false);
//         }
//     }, []);

//     // Optional: avoid flicker while loading
//     if (isAdmin === null) return null;

//     return (
//         <nav>
//             {isAdmin ? (
//                 <a href="/admin">Admin</a>
//             ) : (
//                 <a href="/login">Login</a>
//             )}
//         </nav>
//     );
// }
