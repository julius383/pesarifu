import React, { forwardRef } from "react";
import "./textarea.css";

export interface InputProps {
  id?: string;
  name?: string;
  className?: string;
  rows?: number | undefined;
  //   min?: string | number | undefined;
  maxLength?: number | undefined;
  //   step?: number;
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
  readonly?: boolean;
  onClick?: () => void;
}

const TextArea = forwardRef<HTMLTextAreaElement, InputProps>(
  (
    {
      id = "",
      name = "",
      className,
      rows = 5,
      //   min,
      maxLength,
      //   step,
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
      <textarea
        id={id}
        name={name}
        rows={rows}
        // min={min}
        maxLength={maxLength}
        // step={step}
        value={value}
        ref={ref}
        onChange={onChange}
        placeholder={placeholder}
        className={[
          "textAreaStyle",
          `textAreaStyle--${option}`,
          className,
        ].join(" ")}
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

TextArea.displayName = "TextArea";

export default TextArea;
