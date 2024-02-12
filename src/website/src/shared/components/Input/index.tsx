import React, { forwardRef } from "react";
import "./input.css";

export interface InputProps {
  id?: string;
  name?: string;
  className?: string;
  type?: string;
  min?: number;
  max?: number;
  step?: number;
  value?: any;
  option?: "circle" | "rounded" | "slightlyRounded" | "box" | "line";
  border?: string;
  width?: string;
  padding?: string;
  boxShadow?: string;
  backgroundColor?: string;
  placeholder?: string;
  fontSize?: string;
  color?: string;
  onChange?: any;
  readonly?:boolean;
  onClick?: () => void;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      id = "",
      name = "",
      className,
      type,
      min,
      max,
      step,
      value,
      option,
      border,
      width,
      padding,
      boxShadow,
      backgroundColor,
      placeholder,
      fontSize,
      color,
      onChange,
      readonly = false,
      ...props
    },
    ref
  ) => {
    return (
      <input
        id={id}
        name={name}
        type={type}
        min={min}
        max={max}
        step={step}
        value={value}
        ref={ref}
        onChange={onChange}
        placeholder={placeholder}
        className={["inputStyle", `inputStyle--${option}`, className].join(" ")}
        readOnly={readonly}
        style={{
          border,
          width,
          padding,
          boxShadow,
          backgroundColor,
          fontSize,
          color,
        }}
        {...props}
      />
    );
  }
);

export default Input;
