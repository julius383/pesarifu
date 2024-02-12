import React from "react";
import HeroSection from "./Sections/HeroSection";
import IntroSection from "./Sections/IntroSection";
import BenefitsSection from "./Sections/BenefitsSection";

const HomePage: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-col">
      <HeroSection />
      <IntroSection />
      <BenefitsSection />
    </div>
  );
};

export default HomePage;
