import React from "react";
import "./footer.css";
// import {
//   ISocialMediaProps,
//   social_media_data,
// } from "../../../data/social-media";
// import { Icon } from "@iconify/react";
// import Button from "../Button";
import { Link } from "react-router-dom";
import logo from "../../../logo.svg";

const Footer: React.FC<{}> = () => {
  function getYear() {
    return new Date().getFullYear();
  }

  const openUrl = (url: string) => {
    window.open(url, "_blank", "noreferrer");
  };

  return (
    <footer className="w-full h-full flex flex-row justify-center appBgColorBlack">
      <div className="max-w-[1536px] w-full h-full md:px-7 md-min:px-20 py-[40px] flex flex-col gap-3 justify-between textColorLight relative">
        <div className="w-full flex flex-col justify-between">
          <div></div>

          {/* <div className="flex flex-row items-center z-10">
            {social_media_data.map((item: ISocialMediaProps, index: number) => (
              <Button
                key={index}
                className=" cursor-pointer"
                backgroundColor="transparent"
                type="button"
                option="circle"
                hasIcon
                iconBtn
                title={item.name}
                icon={
                  <Icon
                    icon={item.icon}
                    height={24}
                    color="var(--appColor-light)"
                  />
                }
                onClick={() => openUrl(item.link)}
              />
            ))}
          </div> */}

          <div className="absolute top-[50%] left-[50%] centerAbsolute">
            <Link to="/" className="text-xl font-medium textColorLight">
              <img src={logo} alt="logo" className="w-32 h-12" />
            </Link>
          </div>
        </div>

        {/* Copyright */}
        <div className="w-full flex flex-row justify-between items-center">
          <div className="">
            <p className="text-sm">
              &copy; {getYear()} <a href="https://google.com/"> Pesarifu.</a>
            </p>
          </div>

          <div className="">
            <p className="text-sm">All Rights Reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
