import React, { useEffect } from "react";
import "./navbar.css";
import Button from "../Button";
import { Link } from "react-router-dom";

interface MenuItem {
  name: string;
  route: string;
}

const Navbar: React.FC<{}> = () => {
  const menuItems: MenuItem[] = [
    { name: "Pricing", route: "/subscriptions" },
    { name: "Blog", route: "/blog" },
    { name: "Contact Us", route: "/#contact-us" },
  ];

  return (
    <nav className="w-full absolute top-0 z-30">
      {/* Wide screen navbar */}
      <div className="md:hidden w-full flex flex-row justify-center">
        <div className="max-w-[1536px] w-full px-10 py-5 flex flex-row justify-between items-center">
          <Link to="/" className="text-xl font-medium">
            {/* <img
              src={isDarkMode ? Logo : LogoDark}
              alt="Logo"
              className="h-7 pointer-events-none"
            /> */}
            Logo
          </Link>

          {/* Menu items */}
          <div className="flex flex-row items-center gap-10">
            {menuItems.map((item: MenuItem, index: number) => (
              <>
                <Link to={item.route} className="font-medium text-lg">
                  {item.name}
                </Link>
              </>
            ))}
          </div>

          {/* Auth buttons */}
          <div className="flex flex-row gap-3">
            <div className="">
              <Button
                id="login"
                className=""
                backgroundColor="transparent"
                type="button"
                option="rounded"
                label="Login"
                border="1px solid var(--appColor-dark)"
                onClick={() => {}}
              />
            </div>
            <div className="">
              <Button
                id="login"
                className=""
                backgroundColor="var(--appColor-dark)"
                color="var(--appColor-light)"
                type="button"
                option="rounded"
                label="Get Started"
                border="1px solid var(--appColor-dark)"
                onClick={() => {}}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Mobile navbar */}
      <div className="md-min:hidden w-full p-5 flex flex-row justify-between">
        <Link to="/" className="text-xl font-medium">
          {/* <img
              src={isDarkMode ? Logo : LogoDark}
              alt="Logo"
              className="h-7 pointer-events-none"
            /> */}
          Logo
        </Link>

        <input type="checkbox" id="active" />
        <label
          htmlFor="active"
          // className={
          //   scrollPosition > viewportHeight / 6
          //     ? "menu-btn2-dark"
          //     : "menu-btn2"
          // }
          className="menu-btn"
        >
          <span></span>
        </label>
        <label htmlFor="active" className="close"></label>
        <div className="wrapper">
          <div className="w-full h-full p-10 flex flex-col justify-center text-3xl textColorLight capitalize">
            {/* Menu items */}
            <div className="flex flex-col gap-5">
              {menuItems.map((item: MenuItem, index: number) => (
                <>
                  <Link to={item.route} className="font-medium text-lg">
                    {item.name}
                  </Link>
                </>
              ))}
            </div>

            {/* Auth buttons */}
            <div className="flex flex-row gap-3 mt-10">
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
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
