import type { Metadata } from "next";
import dynamic from "next/dynamic";
import "../styles/globals.css";
import "bootstrap-icons/font/bootstrap-icons.css";

const ChatWidget = dynamic(() => import("../components/ChatWidget"), { ssr: false });

export const metadata: Metadata = {
  title: "MedMind Portal",
  description: "Multi-persona portal for smart medicine box monitoring."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">{children}</div>
        <ChatWidget />
      </body>
    </html>
  );
}
