import React, { PropsWithChildren } from "react";
import PropTypes from "prop-types";
import { Icon } from "@iconify/react";
import InputWithButton from "../InputWithButton";

interface IProps {
  className?: string;
}

const Newsletter: React.FC<PropsWithChildren<IProps>> = (props) => {
  const { className } = props;

  return (
    <div
      className={`md:px-5 px-20 py-10 flex md:flex-col flex-row md-min:justify-between rounded-[15px] appBgColorDark ${className}`}
    >
      <div className="md:w-full w-1/2">
        <h1 className="md:text-xl text-3xl textColorLight">
          Subscribe to our newsletter
        </h1>

        <p className="mt-5 text-lg textColorLight">
          Get the latest product announcements, tips and tricks directly to your
          email
        </p>
      </div>

      <div className="md:w-full w-1/2 flex flex-col md-min:justify-center md-min:items-center">
        <InputWithButton
          id="subscribe"
          className="md:w-full w-3/4 md:mt-10"
          type="text"
          option="line"
          padding="14px 3em 14px 10px"
          backgroundColor="transparent"
          placeholder="Enter your email address here"
          color="var(--appColor-light)"
          boxShadow="0px 1px 0px var(--appColor-light)"
          btnBgColor="transparent"
          hasIcon
          iconBtn
          icon={
            <Icon
              icon="fluent:send-20-regular"
              className=""
              color="var(--appColor-light)"
              fontSize={25}
            />
          }
          onClick={() => {}}
        />
      </div>
    </div>
  );
};

Newsletter.propTypes = {
  children: PropTypes.any,
};

export default Newsletter;
