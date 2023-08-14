import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const MainLayout: React.FC<{}> = () => {
  return (
    <div className="w-full footerCurtain">
      <div className="w-full z-30">
        <Navbar />
      </div>

      <div className="w-full">
        <Outlet />
      </div>

      <div className="w-full h-screen bottom-0 sticky -z-20">
        <Footer />
      </div>
    </div>
  );
};

export default MainLayout;
