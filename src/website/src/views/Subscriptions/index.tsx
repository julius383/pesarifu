import React from "react";
import { ISubscriptionProps, subscriptions_data } from "../../data/subscription";
import SubscriptionCard from "../../shared/components/SubscriptionCard";

const Subscriptions: React.FC<{}> = () => {
  return (
    <div className="w-full flex flex-row justify-center">
      <div className="max-w-[1536px] w-full flex flex-col gap-5 md:px-5 px-20 pt-28 pb-24">
        {/* Subscriptions intro */}
        <div className="w-full flex flex-col items-center">
          <h1 className="md:text-2xl text-4xl font-bold text-center">
            Pesarifu Subscriptions
          </h1>

          <p className="mt-3 text-center text-lg">
            Choose a subscription that suits your needs
          </p>
        </div>

        <div className="w-full mt-10 grid md:grid-cols-1 grid-cols-3 gap-10">
          {subscriptions_data.map(
            (subscription: ISubscriptionProps, index: number) => (
              <SubscriptionCard
                key={index}
                subscription={subscription}
                className="w-full"
              />
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default Subscriptions;
