import React from "react";
import { Parallax } from "react-scroll-parallax";

const IntroSection: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-row justify-center">
      <div
        id="intro-section"
        className="max-w-[1536px] w-full flex flex-col gap-5 md:px-5 px-10 py-24"
      >
        <Parallax
          speed={-10}
          translateY={[-20, 70]}
          translateX={[0, 10]}
          className="w-full py-24"
        >
          <div className="w-full">
            <p className="md:text-2xl text-4xl font-bold">
              Welcome to Pesarifu, where data-driven decisions meet financial
              empowerment!
            </p>
          </div>
        </Parallax>

        <Parallax
          speed={-10}
          translateY={[-20, 70]}
          translateX={[0, -10]}
          className="w-full py-24"
        >
          <div className="w-full py-20 flex flex-row justify-end">
            <p className="md:text-2xl text-4xl font-bold text-right">
              Are you tired of wondering how to maximize the potential of your
              M-Pesa transactions?
            </p>
          </div>
        </Parallax>

        <Parallax speed={11} translateY={[50, 0]} className="py-24">
          <div className="w-full py-20 flex flex-row justify-center">
            <p className="md:text-2xl text-4xl font-bold text-center">
              Look no further! Our cutting-edge analytics platform is designed
              to extract valuable insights from your M-Pesa activities,
              empowering you with the knowledge you need to make informed,
              strategic decisions.
            </p>
          </div>
        </Parallax>
      </div>
    </div>
  );
};

export default IntroSection;
