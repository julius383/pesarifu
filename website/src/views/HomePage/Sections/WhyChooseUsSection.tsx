import React from "react";

const WhyChooseUsSection: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-row justify-center">
      <div className="max-w-[1536px] w-full flex flex-col gap-5 md:px-5 px-10 py-24">
        <div className="w-full py-20">
          <p className="w-1/2 md:text-2xl text-4xl font-bold">
            Welcome to M-Pesa Analytics, where data-driven decisions meet
            financial empowerment!
          </p>
        </div>

        <div className="w-full py-20 flex flex-row justify-end">
          <p className="w-1/2 md:text-2xl text-4xl font-bold text-right">
            Are you tired of wondering how to maximize the potential of your
            M-Pesa transactions?
          </p>
        </div>

        <div className="w-full py-20 flex flex-row justify-center">
          <p className="w-1/2 md:text-2xl text-4xl font-bold text-center">
            Look no further! Our cutting-edge analytics platform is designed to
            extract valuable insights from your M-Pesa activities, empowering
            you with the knowledge you need to make informed, strategic
            decisions.
          </p>
        </div>
      </div>
    </div>
  );
};

export default WhyChooseUsSection;
