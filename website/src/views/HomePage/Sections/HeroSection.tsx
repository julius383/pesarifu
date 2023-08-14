import React from "react";
import Button from "../../../shared/components/Button";
import { Icon } from "@iconify/react";

const HeroSection: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-row justify-center">
      <div className="max-w-[1536px] w-full md-min:h-screen flex md:flex-col flex-row gap-5 md:px-5 px-10 py-24">
        {/* First half of the section */}
        <div className="md:w-full w-1/2 flex flex-col justify-center">
          <h1 className="md:text-2xl text-4xl font-bold">
            Unlock Powerful Insights with M-Pesa Analytics:
          </h1>
          <h3 className="mt-5 md:text-xl text-2xl font-light">
            Harness the Hidden Potential of Your Financial Data!
          </h3>

          <div className="mt-10 flex flex-row items-center md:gap-1 gap-10 text-lg">
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

            <div className="flex flex-row items-center">
              <Button
                id="login"
                className=""
                backgroundColor="transparent"
                color="var(--appColor-dark)"
                type="button"
                option="rounded"
                label="Learn More"
                padding="8px 10px"
                onClick={() => {}}
              />

              <Icon
                icon="mingcute:arrow-right-line"
                height={24}
                color="var(--appColor-dark)"
              />
            </div>
          </div>
        </div>

        {/* Second half */}
        <div className="md:w-full w-1/2 flex flex-col justify-center items-center">
          <div className="w-11/12 h-3/4 rounded-2xl appBgColorDark relative">
            <div className="absolute top-5 left-5">
              <p className="textColorLight">Transactions</p>
              <p className="textColorLight text-2xl">1523</p>

              <div className="mt-5 py-1 px-3 flex flex-row items-center gap-2 rounded-3xl appBgColorLight ">
                <p className="">+35%</p>

                <Icon
                  icon="solar:graph-up-bold"
                  height={24}
                  color="var(--appColor-successText)"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
