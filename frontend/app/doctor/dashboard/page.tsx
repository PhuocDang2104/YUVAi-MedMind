"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function DoctorDashboard() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/doctor/dashboard/overall");
  }, [router]);
  return null;
}
