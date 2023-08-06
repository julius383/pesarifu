import React from "react";

const Footer: React.FC<{}> = () => {
  function getYear() {
    return new Date().getFullYear();
  }

  return (
    <footer className="w-full bottom-0 z-30 largeScreenLayout">
      <div className="nav_footerLargeScreenSize w-full md:px-7 md-min:px-20 py-[40px] flex flex-row justify-between items-center">
        <div className="">
          <p className="text-sm">
            &copy; {getYear()}{" "}
            <a href="https://google.com/"> M-Pesa Analytics.</a>
          </p>
        </div>

        <div className="">
          <p className="text-sm">All Rights Reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
