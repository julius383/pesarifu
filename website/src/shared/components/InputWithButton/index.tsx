import React, { forwardRef } from "react";
import "./inputWithButton.css";
import Button from "../Button";
import Input from "../Input";

interface InputWithButtonProps {
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
  btnBorder?: string;
  btnPadding?: string;
  btnLabel?: string;
  btnBgColor?: string;
  btnTextColor?: string;
  hasIcon?: boolean;
  iconBtn?: boolean;
  icon?: any;
  onChange?: any;
  onClick?: () => void;
}

const InputWithButton = forwardRef<HTMLInputElement, InputWithButtonProps>(
  (
    {
      id = "",
      name = "",
      className,
      type = "text",
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
      btnBorder,
      btnPadding,
      btnLabel,
      btnBgColor,
      btnTextColor,
      hasIcon = false,
      iconBtn = false,
      icon,
      onChange,
      onClick,
      ...props
    },
    ref
  ) => {
    return (
      <div className={["box", className].join(" ")}>
        <Input
          className="activeInputGlow"
          id={id}
          ref={ref}
          name={name}
          type={type}
          min={min}
          max={max}
          step={step}
          value={value}
          option={option}
          border={border}
          boxShadow={boxShadow}
          width={width}
          padding={padding}
          backgroundColor={backgroundColor}
          placeholder={placeholder}
          fontSize={fontSize}
          color={color}
          onChange={onChange}
        />
        <div className={"buttonBox"}>
          <Button
            className="font-quicksand"
            type="button"
            primary
            option={option}
            border={btnBorder}
            padding={btnPadding}
            label={btnLabel}
            fontSize={fontSize}
            backgroundColor={btnBgColor}
            color={btnTextColor}
            hasIcon={hasIcon}
            iconBtn={iconBtn}
            icon={icon}
            onClick={onClick}
          />
        </div>
      </div>
    );
  }
);

export default InputWithButton;
