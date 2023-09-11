import React from "react";
import "../homepage.css";
import { Icon } from "@iconify/react";
import Video from "../../../assets/bg-black-video.mp4";
import { IBenefitsProps, benefits_data } from "../../../data/benefits";

const BenefitsSection: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-row justify-center relative">
      {/* Intro video */}
      <video id="introVid" autoPlay muted loop className="">
        <source src={Video} type="video/mp4" />
      </video>

      <div className="max-w-[1536px] w-full flex md:flex-col flex-row gap-5 md:px-5 px-10 py-24 textColorLight z-10">
        <div className="md:w-full w-1/2 flex flex-col justify-center">
          <p className="md:text-2xl text-4xl font-medium">
            Discover the Power of Pesarifu Insights:
          </p>
        </div>

        <div className="md:w-full w-1/2 flex flex-col justify-center">
          <ul className="flex flex-col gap-10">
            {benefits_data.map((benefit: IBenefitsProps, index: number) => (
              <li className="text-lg flex flex-row gap-3">
                <span>
                  <Icon icon={benefit.icon} height={30} color="inherit" />
                </span>
                {benefit.description}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default BenefitsSection;
