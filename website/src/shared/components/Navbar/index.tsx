import React, { useEffect } from "react";
import "./navbar.css";
const Navbar: React.FC<{}> = () => {
  useEffect(() => {}, []);

  return (
    <nav className="w-full absolute top-0 z-30">
      <div className="w-full largeScreenLayout">
        <div className="nav_footerLargeScreenSize w-full md:px-7 md-min:px-20 py-[40px] flex flex-row justify-between">
          <a href="/" className="my-auto">
            {/* <img
              src={isDarkMode ? Logo : LogoDark}
              alt="Logo"
              className="h-7 pointer-events-none"
            /> */}
            Logo
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
