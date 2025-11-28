"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import type { Route } from "next";

type NavItem = { href: Route; label: string; icon?: React.ReactNode };
type NavGroup = { label: string; icon?: React.ReactNode; items: NavItem[] };

export default function SidebarNav({ groups, title }: { groups: NavGroup[]; title?: string }) {
  const pathname = usePathname();
  const [open, setOpen] = useState<Record<string, boolean>>({});

  return (
    <aside className="sidebar">
      {title ? <div className="muted" style={{ marginBottom: 8, fontWeight: 700 }}>{title}</div> : null}
      {groups.map((group) => {
        const isOpen = open[group.label] ?? true;
        return (
          <div key={group.label} className="nav-group">
            <div
              className="nav-group-header"
              onClick={() => setOpen((prev) => ({ ...prev, [group.label]: !isOpen }))}
            >
              <span>{group.icon}</span>
              <span>{group.label}</span>
              <span style={{ marginLeft: "auto" }}>{isOpen ? "v" : ">"}</span>
            </div>
            {isOpen && (
              <div className="nav-group-content">
                {group.items.map((item) => {
                  const active = pathname === item.href;
                  return (
                    <Link key={item.href} href={item.href} className={`nav-link ${active ? "active" : ""}`}>
                      <span>{item.icon}</span>
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </aside>
  );
}
