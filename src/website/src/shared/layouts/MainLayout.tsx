import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import ContactModal from "../components/ContactModal";


const MainLayout: React.FC<{}> = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const toggleModal = () => {
    setModalOpen((current) => !current);
  }
  return (
    <div className="w-full footerCurtain">
      <div className="w-full fixed z-30">
        <Navbar isOpen={modalOpen} toggle={toggleModal}/>
      </div>

      <div className="w-full">
        <Outlet />
      </div>

      <div className="w-full h-[28rem] md:h-[50rem] bottom-0">
        <Footer />
      </div>
      <div className="w-full">
        <ContactModal isOpen={modalOpen} toggle={toggleModal} />
      </div>
    </div>
  );
};

export default MainLayout;
