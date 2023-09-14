import React from "react";
import "./navbar.css";
import Button from "../Button";
import { Link, useLocation, useNavigate } from "react-router-dom";
import scrollTo from "../../functions/scrollTo";

interface MenuItem {
  name: string;
  route: string;
  type: "link" | "in-page-link";
}

const Navbar: React.FC<{}> = () => {
  const location = useLocation();
  let navigate = useNavigate();

  const menuItems: MenuItem[] = [
    { name: "Pricing", route: "/subscriptions", type: "link" },
    { name: "Blog", route: "/blog", type: "link" },
    { name: "Contact Us", route: "contact-us", type: "in-page-link" },
  ];

  const scrollToInPageLink = (link: string) => {
    if (location.pathname !== "/") {
      navigate("/");
    }

    setTimeout(() => {
      scrollTo(link);
    }, 500);
  };

  return (
    <nav className="w-full absolute top-0 z-30">
      {/* Wide screen navbar */}
      <div className="md:hidden w-full px-10 py-5 flex flex-row justify-center">
        <div className="max-w-[1536px] w-full p-2 flex flex-row justify-between items-center rounded-full appBgColorLight navChipBorder">
          <Link to="/" className="text-xl font-medium ml-5">
            {/* <img
              src={isDarkMode ? Logo : LogoDark}
              alt="Logo"
              className="h-7 pointer-events-none"
            /> */}
            Logo
          </Link>

          {/* Auth buttons */}
          <div className="flex flex-row gap-3">
            {/* Menu items */}
            <div className="flex flex-row items-center gap-5 mr-10">
              {menuItems.map((item: MenuItem, index: number) => (
                <>
                  {item.type === "link" ? (
                    <>
                      <Link to={item.route} className="font-medium text-lg">
                        {item.name}
                      </Link>
                    </>
                  ) : (
                    <>
                      <p
                        className="font-medium text-lg cursor-pointer"
                        onClick={() => scrollToInPageLink(item.route)}
                      >
                        {item.name}
                      </p>
                    </>
                  )}
                </>
              ))}
            </div>

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
      <div className="md-min:hidden p-5">
        <div className="w-full px-5 py-2 flex flex-row justify-between rounded-full appBgColorLight navChipBorder">
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
      </div>
    </nav>
  );
};

export default Navbar;
