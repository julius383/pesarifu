import React, { PropsWithChildren } from "react";
import PropTypes from "prop-types";
import "./dropdown.css";

export interface DropdownProps {
  id?: string;
  name?: string;
  className?: string;
  border?: string;
  boxShadow?: string;
  width?: string;
  backgroundColor?: string;
  padding?: string;
  fontSize?: string;
  color?: string;
  option?: "rounded" | "slightlyRounded" | "box" | "line";
  value?: any;
  onChange?: any;
  // onClick?: () => void;
}

const Dropdown: React.FC<PropsWithChildren<DropdownProps>> = ({
  children,
  id = "",
  name = "",
  className,
  border,
  boxShadow,
  width,
  backgroundColor,
  padding,
  fontSize,
  color,
  option,
  value,
  onChange,
  ...props
}) => {
  return (
    <div
      className={["dropdownStyle", `dropdownStyle--${option}`, `${className}`].join(" ")}
      style={{ border, boxShadow, width, backgroundColor }}
    >
      <select
        id={id}
        name={name}
        style={{
          padding,
          fontSize,
          color,
        }}
        value={value}
        onChange={onChange}
        {...props}
      >
        {children}
      </select>
      <span className={"focus"}></span>
    </div>
  );
};

Dropdown.propTypes = {
  children: PropTypes.any,
};

export default Dropdown;
