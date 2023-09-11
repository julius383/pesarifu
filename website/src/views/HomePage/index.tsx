import React from "react";
import HeroSection from "./Sections/HeroSection";
import IntroSection from "./Sections/IntroSection";
import BenefitsSection from "./Sections/BenefitsSection";
import ContactUsSection from "./Sections/ContactUsSection";

const HomePage: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-col">
      <HeroSection />
      <IntroSection />
      <BenefitsSection />
      <ContactUsSection />
    </div>
  );
};

export default HomePage;
