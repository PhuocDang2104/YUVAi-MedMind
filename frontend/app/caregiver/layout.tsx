import "../../styles/caregiver.css";
import CaregiverNav from "../../components/CaregiverNav";
import Topbar from "../../components/Topbar";

export const metadata = {
  title: "Caregiver Portal"
};

export default function CaregiverLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="caregiver-page">
      <Topbar persona="Caregiver" name="Thao Nguyen" role="Caregiver" />
      {children}
      <CaregiverNav />
    </div>
  );
}
