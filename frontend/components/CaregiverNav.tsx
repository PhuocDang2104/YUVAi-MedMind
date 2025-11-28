"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { Route } from "next";

const items: { href: Route; label: string }[] = [
  { href: "/caregiver/home", label: "Home" },
  { href: "/caregiver/health-log", label: "Health Log" },
  { href: "/caregiver/medication", label: "Medication" },
  { href: "/caregiver/alerts", label: "Alerts" },
  { href: "/caregiver/profile", label: "Profile" }
];

export default function CaregiverNav() {
  const pathname = usePathname();
  return (
    <nav className="nav-bottom">
      {items.map((item) => {
        const active = pathname === item.href;
        return (
          <Link key={item.href} href={item.href} className={active ? "active" : ""}>
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
