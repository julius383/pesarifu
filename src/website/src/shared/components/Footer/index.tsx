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
    <footer className="w-full h-full text-gray-400 bg-gray-900">
        <div className="flex flex-row md:flex-col justify-center">
            <div className="basis-1/3 m-4 ml-6">
                <div className="flex flex-col mt-4">
                      <Link to="/" className="mb-3">
                        <img src={logo} alt="logo" className="h-8" />
                      </Link>
                        <p className="text-md w-5/6">
                            Pesarifu is dedicated to empowering individuals
                            with actionable insights derived from their financial transactions.
                            Our cutting-edge analytics platform transforms transaction data into
                            strategic advantages, guiding users towards informed financial
                            decisions.
                        </p>
                </div>
            </div>
            <div className="basis-1/3 m-4 mt-10">
                <div className="flex flex-col mb-1">
                    <h4 className="font-bold mb-2 text-xl text-cyan-500">Company</h4>
                    <h5 className="font-bold text-lg mb-0.5">Pesarifu</h5>
                    <p className="italic text-gray-500 mb-1">Nairobi, Kenya</p>
                    <div className="flex flex-row mb-1">
                      <svg
                         xmlns="http://www.w3.org/2000/svg"
                         className="justify-center icon icon-tabler icon-tabler-mail-filled"
                         width="28" height="28"
                         viewBox="0 0 24 24"
                         stroke-width="1.5"
                         stroke="#9ca3af"
                         fill="none"
                         stroke-linecap="round"
                         stroke-linejoin="round">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                          <path d="M22 7.535v9.465a3 3 0 0 1 -2.824 2.995l-.176 .005h-14a3 3 0 0 1 -2.995 -2.824l-.005 -.176v-9.465l9.445 6.297l.116 .066a1 1 0 0 0 .878 0l.116 -.066l9.445 -6.297z" stroke-width="0" fill="currentColor" />
                          <path d="M19 4c1.08 0 2.027 .57 2.555 1.427l-9.555 6.37l-9.555 -6.37a2.999 2.999 0 0 1 2.354 -1.42l.201 -.007h14z" stroke-width="0" fill="currentColor" />
                      </svg>
                      <Link to="mailto:info@pesarifu.com" className="font-medium ml-3 ">
                          info@pesarifu.com
                      </Link>
                    </div>
                </div>
            </div>
            <div className="basis-1/3 m-4 mt-10">
                <div className="flex flex-col mb-1">
                    <h4 className="font-bold mb-2 text-xl text-cyan-500">Quick Links</h4>
                    <Link to="https://app.pesarifu.com/" className="font-medium">
                        Get Started
                    </Link>
                    <Link to="https://app.pesarifu.com/demo" className="font-medium">
                        See Demo
                    </Link>
                </div>
            </div>
    </div>
      <div className="w-full items-center m-6 mt-8 flex flex-col">
        <p className="text-l">
          Copyright &copy; {getYear()} <a href="https://pesarifu.com/"> Pesarifu.</a>
        </p>
        <p className="text-l">All Rights Reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
