import React from "react";
import HeroSection from "./Sections/HeroSection";
import IntroSection from "./Sections/IntroSection";

const HomePage: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-col">
      <HeroSection />
      <IntroSection />
    </div>
  );
};

export default HomePage;
