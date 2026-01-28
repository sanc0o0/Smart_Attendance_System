"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  useEffect(() => {
    const raw = localStorage.getItem("adminAuth");
    if (!raw) {
      router.replace("/login");
      return;
    }

    const auth = JSON.parse(raw);
    if (Date.now() > auth.expiresAt) {
      localStorage.removeItem("adminAuth");
      router.replace("/login");
    }
  }, []);

  return <>{children}</>;
}
