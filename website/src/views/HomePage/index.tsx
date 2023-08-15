import React from "react";
import HeroSection from "./Sections/HeroSection";
import IntroSection from "./Sections/IntroSection";
import BenefitsSection from "./Sections/BenefitsSection";
import WhyChooseUsSection from "./Sections/WhyChooseUsSection";

const HomePage: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-col">
      <HeroSection />
      <IntroSection />
      <BenefitsSection />
      <WhyChooseUsSection />
    </div>
  );
};

export default HomePage;
