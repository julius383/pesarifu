import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const MainLayout: React.FC<{}> = () => {
  return (
    <div className="w-full">
      <div className="w-full z-30">
        <Navbar />
      </div>

      <div className="w-full">
        <Outlet />
      </div>

      <div className="w-full z-30">
        <Footer />
      </div>
    </div>
  );
};

export default MainLayout;
