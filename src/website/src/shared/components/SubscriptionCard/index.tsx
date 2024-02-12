import React, { PropsWithChildren } from "react";
import PropTypes from "prop-types";
import "./subscription.css";
import { ISubscriptionProps } from "../../../data/subscription";
import numbersWithCommas from "../../functions/numbersWithCommas";
import Button from "../Button";

interface IProps {
  className?: string;
  subscription: ISubscriptionProps;
}

const SubscriptionCard: React.FC<PropsWithChildren<IProps>> = (props) => {
  const { className, subscription } = props;

  const getSubscription = () => {
    alert("Hello there");
  };

  return (
    <div
      className={`p-5 flex flex-col rounded-[30px] neumorphism subscriptionCard ${className}`}
    >
      <h2 className="text-2xl text-center">{subscription.name}</h2>

      <div className="w-full my-5 flex flex-row justify-center">
        <div className="w-1/6 h-[1px] subscriptionSeparator rounded-xl"></div>
      </div>

      <p className="text-3xl text-center">
        Ksh. {numbersWithCommas(subscription.price)}{" "}
        <span className="text-sm">/ month</span>
      </p>

      <div className="h-full mt-10 mb-5 flex flex-col justify-between">
        <ul className="">
          {subscription.contents.map((content: string, index: number) => (
            <li key={index} className="text-center">
              {content}
            </li>
          ))}
        </ul>

        <div className="md-min:col-span-2 mt-10 text-center">
          <Button
            id="subscribe"
            className=""
            backgroundColor="var(--appColor-dark)"
            color="var(--appColor-light)"
            type="button"
            option="rounded"
            label="Subscribe"
            border="1px solid var(--appColor-dark)"
            onClick={() => {
              getSubscription();
            }}
          />
        </div>
      </div>
    </div>
  );
};

SubscriptionCard.propTypes = {
  children: PropTypes.any,
};

export default SubscriptionCard;
