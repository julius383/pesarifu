import React, { useState } from "react";
import Button from "../Button"
import "./navbar.css";
import { Link, useLocation, useNavigate } from "react-router-dom";
import scrollTo from "../../functions/scrollTo";
import logo from "../../../logo.svg";

interface MenuItem {
  name: string;
  route: string;
  type: "link" | "in-page-link";
}

interface ModalProps {
  isOpen: boolean;
  toggle: () => void;
}

const Navbar: React.FC<ModalProps> = ({ isOpen, toggle }) => {
  const location = useLocation();
  let navigate = useNavigate();

  const menuItems: MenuItem[] = [
    // { name: "Pricing", route: "/subscriptions", type: "link" },
    { name: "Home", route: "/", type: "link" },
    { name: "Blog", route: "/blog", type: "link" },
  ];

  const scrollToInPageLink = (link: string) => {
    if (location.pathname !== "/") {
      navigate("/");
    }

    setTimeout(() => {
      scrollTo(link);
    }, 500);
  };

  const [isActive, setIsActive] = useState(false);

  const handleClick = () => {
    setIsActive((current) => !current);
  };


  return (
    <nav className="w-full absolute top-0 z-30">
      {/* Wide screen navbar */}
      <div className="md:hidden w-full px-10 py-5 flex flex-row justify-center">
        <div className="max-w-[1536px] w-full p-2 flex flex-row justify-between items-center rounded-full appBgColorLight navChipBorder">
          <Link to="/" className="ml-5">
            <img src={logo} alt="logo" className="w-28 h-12" />
          </Link>

          {/* Auth buttons */}
          <div className="flex flex-row gap-3">
            {/* Menu items */}
            <div className="flex flex-row items-center gap-5 mr-10">
              {menuItems.map((item: MenuItem, index: number) => (
                <>
                  {item.type === "link" ? (
                    <>
                      <Link to={item.route} className="font-semibold text-lg" >
                        {item.name}
                      </Link>
                    </>
                  ) : (
                    <>
                      <p
                        className="font-semibold text-lg cursor-pointer"
                        onClick={() => scrollToInPageLink(item.route)}
                      >
                        {item.name}
                      </p>
                    </>
                  )}
                </>
              ))}
              <Link to="#contactModal" className="font-medium font-semibold text-lg" onClick={() => { handleClick(); toggle(); }}>
                {"Contact Us"}
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile navbar */}
      <div className="md-min:hidden p-5 w-full flex flex-row justify-between">
        <div className="w-full px-5 py-2 flex flex-row justify-between items-center rounded-full appBgColorLight navChipBorder">
          <Link to="/">
            <img src={logo} alt="logo" className="object-none w-20 h-5" />
          </Link>
          <button onClick={handleClick}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="icon icon-tabler icon-tabler-menu-2"
              width="34"
              height="34"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="#000000"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none" />
              <path d="M4 6l16 0" />
              <path d="M4 12l16 0" />
              <path d="M4 18l16 0" />
            </svg>
          </button>

          <div className="wrapper" style={{ right: isActive ? "0" : "-100%" }}>
            <div className="w-full h-full p-10 flex flex-col justify-center text-3xl textColorLight capitalize">
              <button
                onClick={handleClick}
                className="absolute top-0 right-0 h-16 w-16"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="icon icon-tabler icon-tabler-x"
                  width="34"
                  height="34"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  fill="none"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path d="M18 6l-12 12" />
                  <path d="M6 6l12 12" />
                </svg>
              </button>
              {/* Menu items */}
              <div className="flex flex-col gap-5">
                <Link to="/" className="mb-3" onClick={handleClick}>
                  <img src={logo} alt="logo" className="w-28 h-12" />
                </Link>
                <hr/>
                {menuItems.map((item: MenuItem, index: number) => (
                  <>
                    <Link to={item.route} className="font-medium text-lg" onClick={handleClick}>
                      {item.name}
                    </Link>
                  </>
                ))}
                <Link to="#contactModal" className="font-medium text-lg" onClick={() => { handleClick(); toggle(); }}>
                  {"Contact Us"}
                </Link>
              </div>

              {/* Auth buttons */}
              {/* <div className="flex flex-row gap-3 mt-10">
                <div className="">
                  <Button
                    id="login"
                    className="text-lg"
                    backgroundColor="transparent"
                    type="button"
                    option="rounded"
                    label="Login"
                    border="1px solid var(--appColor-light)"
                    onClick={() => {}}
                  />
                </div>

                <div className="">
                  <Button
                    id="login"
                    className="text-lg"
                    backgroundColor="var(--appColor-light)"
                    color="var(--appColor-dark)"
                    type="button"
                    option="rounded"
                    label="Get Started"
                    border="1px solid var(--appColor-dark)"
                    onClick={() => {}}
                  />
                </div>
              </div> */}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
