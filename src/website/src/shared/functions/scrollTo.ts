const scrollTo = (section: string) => {
  const element = document.getElementById(section);
  element && element.scrollIntoView({ behavior: "smooth" });
};

export default scrollTo;
